# src/schemas/user.py

from pydantic import BaseModel, EmailStr
from datetime import datetime

# Importamos o Enum que acabamos de definir no modelo
from src.models.user import UserRole 

# Schema base para dados de usuário
class UserBase(BaseModel):
    email: EmailStr
    display_name: str | None = None

# Schema para criar um novo usuário (usado internamente)
class UserCreate(UserBase):
    firebase_uid: str
    
# Schema para ler/retornar dados de usuário
class UserRead(UserBase):
    id: int
    firebase_uid: str
    role: UserRole  # <<< Usamos o Enum aqui para validação
    organization_id: int | None = None
    created_at: datetime

    class Config:
        from_attributes = True # Padrão Pydantic v2

# --- NOVO SCHEMA ---
# Schema para o corpo (body) da requisição de atualização de papel
class UserRoleUpdate(BaseModel):
    role: UserRole # O frontend deve enviar a nova role