# src/services/search_service.py

import os
from sqlalchemy.orm import Session
from sqlalchemy import select, text
from sentence_transformers import SentenceTransformer
from litellm import completion
from src.core.config import settings

from src.models.document import DocumentChunk
from src.schemas.search import SearchResultChunk, QAResponse

# Configura a chave de API da Groq
os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY

# EMBEDDINGS (Hugging Face Local)
MODEL_NAME = 'paraphrase-multilingual-MiniLM-L12-v2'
embedding_model = SentenceTransformer(MODEL_NAME)


def semantic_search(
    db: Session, 
    query: str, 
    organization_id: int, 
    top_k: int = 5
) -> list[SearchResultChunk]:
    """
    Realiza a busca semântica no banco de dados.
    """
    
    # --- 1. A LINHA CORRIGIDA ESTÁ AQUI ---
    # Gera o embedding da consulta do usuário.
    query_embedding = embedding_model.encode(query).tolist()
    # ------------------------------------

    # 2. Executar a consulta SQL com pgvector
    db.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

    sql_query = text(
        """
        SELECT 
            dc.document_id,
            dc.page_number,
            dc.content,
            dc.embedding <=> CAST(:query_embedding AS vector) AS similarity
        FROM 
            document_chunks AS dc
        JOIN 
            documents AS d ON dc.document_id = d.id
        WHERE 
            d.organization_id = :organization_id
        ORDER BY 
            similarity
        LIMIT :top_k
        """
    )
    
    # Executa a query
    results = db.execute(
        sql_query,
        {
            "query_embedding": str(query_embedding), # Agora esta variável existe
            "organization_id": organization_id,
            "top_k": top_k
        }
    ).fetchall()

    # 3. Formata os resultados
    search_results = [
        SearchResultChunk(
            document_id=row.document_id,
            page_number=row.page_number,
            content=row.content,
            similarity=row.similarity
        )
        for row in results
    ]
    return search_results


def answer_question(
    db: Session, 
    query: str, 
    organization_id: int
) -> QAResponse:
    """
    Realiza o fluxo de RAG (Retrieval-Augmented Generation).
    """
    
    # 1. Retrieve: Busca os 3 chunks mais relevantes
    # Esta chamada agora funcionará corretamente.
    context_chunks = semantic_search(
        db, query=query, organization_id=organization_id, top_k=3
    )
    
    if not context_chunks:
        return QAResponse(
            answer="Não encontrei informações relevantes sobre este tópico nos seus documentos.",
            sources=[]
        )

    # 2. Augment: Cria o contexto e o prompt
    context_str = "\n\n---\n\n".join(
        [f"Trecho (Página {chunk.page_number}, Documento {chunk.document_id}):\n{chunk.content}" 
         for chunk in context_chunks]
    )
    
    system_prompt = (
        "Você é um assistente de IA especialista em análise de documentos.\n"
        "Sua tarefa é responder a pergunta do usuário baseando-se *apenas* no contexto fornecido.\n"
        "Se a resposta não estiver no contexto, diga 'Não encontrei informações sobre isso nos documentos.'\n"
        "Cite suas fontes, se possível, mencionando a página."
    )
    
    user_prompt = f"Contexto:\n{context_str}\n\n---\n\nPergunta do Usuário: {query}"
    
    # 3. Generate: Chama o LLM (Groq)
    try:
        response = completion(
            model="groq/mixtral-8x7b-32768", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1
        )
        
        answer = response.choices[0].message.content
        
    except Exception as e:
        print(f"Erro ao chamar o LLM (Groq): {e}")
        answer = "Ocorreu um erro ao gerar a resposta. Tente novamente."

    return QAResponse(answer=answer, sources=context_chunks)