# src/api/deps.py

from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.db.session import SessionLocal
from src.core import security
from src.models import user as user_model
from src.services import user_service

# Este objeto define o "esquema" de segurança para o FastAPI.
# Ele informa ao Swagger/docs que ele deve esperar um Bearer Token (JWT).
# A 'tokenUrl' é simbólica, pois nosso token vem do Firebase,
# mas é necessária para a configuração.
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/register" 
)

def get_db() -> Generator:
    """
    Dependência que gera uma nova sessão de banco de dados (SessionLocal)
    para cada requisição. Usa um 'yield' para injetar a sessão no endpoint
    e garante que 'db.close()' seja chamado ao final, mesmo se um erro ocorrer.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> user_model.User:
    """
    Dependência para obter o usuário atual.
    1. Obtém o token string do header 'Authorization'.
    2. Valida o token com o Firebase Admin.
    3. Busca o usuário correspondente no nosso banco de dados PostgreSQL.
    4. Levanta um erro 404 se o usuário não estiver registrado no nosso banco.
    """
    decoded_token = security.validate_firebase_token(token)
    firebase_uid = decoded_token.get("uid")
    
    user = user_service.get_user_by_firebase_uid(db, firebase_uid=firebase_uid)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado no banco de dados. Por favor, registre-se.",
        )
    return user

def get_current_admin_user(
    current_user: user_model.User = Depends(get_current_user),
) -> user_model.User:
    """
    Dependência que protege um endpoint, exigindo que o usuário tenha a role 'admin'.
    Depende de 'get_current_user' para primeiro obter o usuário.
    Levanta um erro 403 (Forbidden) se o usuário não for admin.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Esta ação requer privilégios de administrador."
        )
    return current_user

def get_current_editor_user(
    current_user: user_model.User = Depends(get_current_user),
) -> user_model.User:
    """
    Dependência que protege um endpoint, exigindo que o usuário tenha
    pelo menos a role 'editor'. Permite 'admin' e 'editor'.
    Levanta um erro 403 (Forbidden) se o usuário for apenas 'viewer'.
    """
    if current_user.role not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Esta ação requer privilégios de editor ou administrador."
        )
    return current_user