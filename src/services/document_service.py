import os
from sqlalchemy.orm import Session
from fastapi import UploadFile

from src.models import document as doc_model
from src.schemas import document as doc_schema
from src.models.user import User

# Define um diretório local para salvar os uploads. Em produção, isso seria um bucket S3.
UPLOAD_DIRECTORY = "./uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

def save_uploaded_file(upload_file: UploadFile) -> str:
    """
    Salva o arquivo enviado em um diretório local e retorna o caminho.
    """
    file_path = os.path.join(UPLOAD_DIRECTORY, upload_file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(upload_file.file.read())
    return file_path

def create_document(db: Session, upload_file: UploadFile, current_user: User) -> doc_model.Document:
    """
    Cria a entrada do documento no banco de dados.
    """
    # Salva o arquivo fisicamente
    file_path = save_uploaded_file(upload_file)

    # Cria o objeto Pydantic com os dados do documento
    doc_in = doc_schema.DocumentCreate(
        file_name=upload_file.filename,
        file_path=file_path,
        file_size=upload_file.size,
        mime_type=upload_file.content_type,
        organization_id=current_user.organization_id,
        uploaded_by_id=current_user.id
    )
    
    # Cria o modelo SQLAlchemy e salva no banco
    db_document = doc_model.Document(**doc_in.dict())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_documents_by_organization(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    """
    Retorna uma lista de documentos de uma organização específica.
    """
    return db.query(doc_model.Document).filter(
        doc_model.Document.organization_id == organization_id
    ).offset(skip).limit(limit).all()