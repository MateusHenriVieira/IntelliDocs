from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session

from src.api import deps
from src.models.user import User
from src.schemas import document as doc_schema
from src.services import document_service
# from src.tasks.document_tasks import process_document_task # Descomente quando a task estiver pronta

router = APIRouter()

@router.post("/upload", response_model=doc_schema.DocumentRead)
def upload_document(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    file: UploadFile = File(...)
):
    """
    Endpoint para fazer o upload de um novo documento.
    Salva o arquivo e cria o registro no banco.
    """
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário não está associado a uma organização."
        )
    
    # Cria o documento no banco de dados
    document = document_service.create_document(db=db, upload_file=file, current_user=current_user)
    
    # Dispara a tarefa em background para processamento de IA (OCR, embeddings)
    # process_document_task.delay(document_id=document.id)
    
    return document


@router.get("/", response_model=List[doc_schema.DocumentRead])
def list_documents(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """
    Endpoint para listar todos os documentos da organização do usuário logado.
    """
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário não está associado a uma organização."
        )
        
    documents = document_service.get_documents_by_organization(
        db, organization_id=current_user.organization_id, skip=skip, limit=limit
    )
    return documents