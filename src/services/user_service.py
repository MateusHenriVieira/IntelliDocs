# src/services/user_service.py

from sqlalchemy.orm import Session
from src.models import user as user_model
from src.schemas import user as user_schema

# Importamos o Enum de papéis
from src.models.user import UserRole

def get_user_by_firebase_uid(db: Session, firebase_uid: str):
    return db.query(user_model.User).filter(user_model.User.firebase_uid == firebase_uid).first()

def create_user(db: Session, user_in: user_schema.UserCreate, organization_id: int):
    """
    Cria um novo usuário e o associa a uma organização.
    Define o primeiro usuário como 'ADMIN' da organização.
    """
    db_user = user_model.User(
        firebase_uid=user_in.firebase_uid,
        email=user_in.email,
        display_name=user_in.display_name,
        organization_id=organization_id,
        role=UserRole.ADMIN  # <<< Usamos o Enum aqui
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users_by_organization(db: Session, organization_id: int):
    """
    Retorna uma lista de todos os usuários de uma organização específica.
    """
    return db.query(user_model.User).filter(
        user_model.User.organization_id == organization_id
    ).all()

# --- NOVA FUNÇÃO 1 ---
def get_user_by_id(db: Session, user_id: int) -> user_model.User | None:
    """
    Busca um usuário pelo seu ID primário (integer).
    """
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()

# --- NOVA FUNÇÃO 2 ---
def update_user_role(db: Session, db_user: user_model.User, new_role: UserRole) -> user_model.User:
    """
    Atualiza o papel (role) de um usuário no banco de dados.
    """
    db_user.role = new_role
    db.commit()
    db.refresh(db_user)
    return db_user