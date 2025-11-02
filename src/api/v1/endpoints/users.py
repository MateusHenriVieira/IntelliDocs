# src/api/v1/endpoints/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Importações do nosso projeto
from src.api import deps
from src.models import user as user_model
from src.schemas import user as user_schema
from src.services import user_service
from src.models.user import UserRole # Importamos o Enum

# Cria o roteador para este módulo
router = APIRouter()


@router.get("/me", response_model=user_schema.UserRead)
def read_user_me(
    current_user: user_model.User = Depends(deps.get_current_user),
):
    """
    Endpoint para obter os dados do usuário atualmente autenticado.
    """
    return current_user


@router.get("/", response_model=List[user_schema.UserRead])
def list_users_in_organization(
    db: Session = Depends(deps.get_db),
    # Esta dependência garante que só um admin pode chamar este endpoint.
    admin_user: user_model.User = Depends(deps.get_current_admin_user)
):
    """
    (Rota Protegida - Admin) 
    Lista todos os usuários na organização do administrador que está fazendo a requisição.
    """
    users = user_service.get_users_by_organization(
        db, organization_id=admin_user.organization_id
    )
    return users


# --- NOVO ENDPOINT ---
@router.patch("/{user_id}/role", response_model=user_schema.UserRead)
def update_user_role(
    user_id: int,  # O ID do usuário que queremos modificar
    role_update: user_schema.UserRoleUpdate, # O corpo da requisição com a nova role
    db: Session = Depends(deps.get_db),
    admin_user: user_model.User = Depends(deps.get_current_admin_user)
):
    """
    (Rota Protegida - Admin) 
    Altera o papel (role) de um usuário específico na organização.
    """
    
    # 1. Busca o usuário que será modificado
    user_to_update = user_service.get_user_by_id(db, user_id=user_id)

    # 2. Verifica se o usuário existe
    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário a ser atualizado não foi encontrado."
        )
    
    # 3. Verifica se o usuário pertence à mesma organização do admin
    if user_to_update.organization_id != admin_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não pode modificar usuários de outra organização."
        )

    # 4. Regra de negócio: Proibir o admin de rebaixar a si mesmo
    if user_to_update.id == admin_user.id and role_update.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Um administrador não pode rebaixar o próprio papel."
        )

    # 5. Se tudo estiver ok, atualiza o papel
    updated_user = user_service.update_user_role(
        db=db, db_user=user_to_update, new_role=role_update.role
    )
    
    return updated_user