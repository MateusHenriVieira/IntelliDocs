import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, status

from src.core.config import settings

# Inicializa o Firebase Admin SDK
# Em um ambiente de produção, use um Service Account Key.
# Para desenvolvimento local, ele pode usar as credenciais do ambiente.
try:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': settings.FIREBASE_PROJECT_ID,
    })
except Exception:
     # Evita erro de reinicialização durante o --reload do uvicorn
    if not firebase_admin._apps:
        firebase_admin.initialize_app()


def validate_firebase_token(token: str) -> dict:
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )