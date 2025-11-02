from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api import deps
from src.core.security import validate_firebase_token
from src.schemas.token import TokenData
from src.schemas.user import UserCreate, UserRead
from src.services import user_service

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    token_data: TokenData
):
    """
    Recebe um token do Firebase, valida, e cria um novo usuário no banco local
    se ele ainda não existir.
    """
    decoded_token = validate_firebase_token(token_data.access_token)
    
    firebase_uid = decoded_token.get("uid")
    email = decoded_token.get("email")
    display_name = decoded_token.get("name")

    # Verifica se o usuário já existe
    user = user_service.get_user_by_firebase_uid(db, firebase_uid=firebase_uid)
    if user:
        # Se já existe, podemos apenas retorná-lo ou atualizar suas informações
        return user

    # Se não existe, cria o novo usuário
    user_in = UserCreate(
        firebase_uid=firebase_uid,
        email=email,
        display_name=display_name
    )
    new_user = user_service.create_user(db, user_in=user_in)
    
    return new_user