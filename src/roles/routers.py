from fastapi import APIRouter, Depends
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_bearer import JWTBearer
from src.auth.services import check_permission
from src.database import get_async_session
from src.models import Role
from src.roles.schemas import RoleCreate
from src.roles.services import RoleService

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    # responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_root(session: AsyncSession = Depends(get_async_session),
                    current_user: str = Depends(JWTBearer())):
    check_permission("read_role", current_user)
    """
    Get all roles
    """
    return await RoleService.get_roles(session)


@router.post("/")
async def create_role(role: RoleCreate,
                      session: AsyncSession = Depends(get_async_session),
                      current_user: str = Depends(JWTBearer())):
    check_permission("create_role", current_user)
    """
    Create role
    """
    return await RoleService.create_role(role, session)


@router.get("/{role_id}")
async def read_role(role_id: int,
                    session: AsyncSession = Depends(get_async_session),
                    current_user: str = Depends(JWTBearer())):
    check_permission("read_role", current_user)
    """
    Get role by id
    """
    return await RoleService.get_role(role_id, session)


@router.patch("/{role_id}")
async def update_role(role_id: int,
                      role: RoleCreate,
                      session: AsyncSession = Depends(get_async_session),
                      current_user: str = Depends(JWTBearer())):
    check_permission("update_role", current_user)
    """
    Update role by id
    """
    return await RoleService.update_role(role_id, role, session)


@router.delete("/{role_id}")
async def delete_role(role_id: int,
                      session: AsyncSession = Depends(get_async_session),
                      current_user: str = Depends(JWTBearer())):
    check_permission("delete_role", current_user)
    """
    Delete role by id
    """
    return await RoleService.delete_role(role_id, session)
