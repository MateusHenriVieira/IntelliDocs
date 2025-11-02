import fitz  # PyMuPDF
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer

from .celery_app import celery_app
from src.db.session import SessionLocal
from src.services import document_servicedocker
from src.models.document import Document, DocumentChunk

# --- Carregamento do Modelo de IA ---
# O modelo é carregado UMA VEZ quando o worker inicia,
# economizando muito tempo e memória.
MODEL_NAME = 'paraphrase-multilingual-MiniLM-L12-v2'
print(f"Carregando modelo de embedding: {MODEL_NAME}...")
embedding_model = SentenceTransformer(MODEL_NAME)
print("Modelo de embedding carregado com sucesso.")

def get_db() -> Session:
    return SessionLocal()

@celery_app.task(name="process_document_task")
def process_document_task(document_id: int):
    """
    Tarefa assíncrona para processar um documento:
    1. Atualiza o status para 'PROCESSING'
    2. Lê o arquivo PDF
    3. Extrai o texto página por página
    4. Gera o embedding para o texto de cada página
    5. Salva o chunk (texto, página, embedding) no banco
    6. Atualiza o status para 'COMPLETED' ou 'FAILED'
    """
    print(f"[TASK INICIADA] Processando documento ID: {document_id}")
    db = get_db()
    
    try:
        # 1. Obter o documento e atualizar status
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            print(f"[ERRO] Documento ID: {document_id} não encontrado.")
            return

        doc.status = "PROCESSING"
        db.commit()
        print(f"[STATUS] Documento ID: {doc.id} - Status: PROCESSING")

        # 2. Abrir o arquivo PDF
        pdf_document = fitz.open(doc.file_path)
        
        chunks_para_salvar = []

        # 3. Iterar página por página
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            page_text = page.get_text("text") # Extrai o texto
            
            if not page_text.strip(): # Pula páginas em branco
                continue

            # 4. Gerar o embedding para o texto da página
            # O 'tolist()' converte o vetor numpy em uma lista Python
            embedding = embedding_model.encode(page_text).tolist()

            # 5. Criar o objeto DocumentChunk
            new_chunk = DocumentChunk(
                document_id=doc.id,
                content=page_text,
                page_number=page_num + 1,  # Páginas são 1-indexadas para o usuário
                embedding=embedding
            )
            chunks_para_salvar.append(new_chunk)

        pdf_document.close()

        # Salva todos os chunks no banco de uma vez (mais eficiente)
        db.bulk_save_objects(chunks_para_salvar)
        
        # 6. Atualizar status para COMPLETED
        doc.status = "COMPLETED"
        db.commit()
        print(f"[STATUS] Documento ID: {doc.id} - Status: COMPLETED. {len(chunks_para_salvar)} chunks processados.")

    except Exception as e:
        db.rollback()
        # 6. Atualizar status para FAILED
        doc = db.query(Document).filter(Document.id == document_id).first()
        if doc:
            doc.status = "FAILED"
            db.commit()
        print(f"[ERRO] Falha ao processar o documento ID: {document_id}. Erro: {e}")
    finally:
        db.close()
        
    return f"Documento {document_id} processado."