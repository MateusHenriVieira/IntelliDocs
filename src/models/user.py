# src/models/user.py

import enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SqlEnum # Importamos o Enum do SQLAlchemy

from src.db.base import Base

# --- 1. Definimos os papéis (roles) usando um Enum do Python ---
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"
# -----------------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firebase_uid = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    display_name = Column(String, nullable=True)
    
    # --- 2. Atualizamos a coluna 'role' ---
    # Agora ela usa o Enum, com "viewer" como padrão.
    role = Column(SqlEnum(UserRole), nullable=False, default=UserRole.VIEWER)
    # -------------------------------------
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship("Organization", back_populates="users")