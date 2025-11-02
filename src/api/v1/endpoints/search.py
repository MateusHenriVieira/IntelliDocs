from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api import deps
from src.models.user import User
from src.schemas.search import SearchQuery, SearchResponse
from src.services import search_service

router = APIRouter()

@router.post("/", response_model=SearchResponse)
def search_documents(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    search_query: SearchQuery
):
    """
    Endpoint de busca semântica.
    Recebe uma query de texto e retorna os chunks de documento mais relevantes
    da organização do usuário.
    """
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário não está associado a uma organização."
        )

    results = search_service.semantic_search(
        db=db,
        query=search_query.query,
        organization_id=current_user.organization_id,
        top_k=search_query.top_k
    )
    
    return SearchResponse(results=results)