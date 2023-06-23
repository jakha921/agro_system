from fastapi import APIRouter, Depends
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models import Permission
from src.permissions import schemas
from src.permissions.services import PermissionService

router = APIRouter(
    prefix="/permissions",
    tags=["permissions"],
    # responses={404: {"description": "Not found"}},
)
permission_service = PermissionService(Permission)


@router.get("/")
async def get_permissions(session: AsyncSession = Depends(get_async_session)):
    return await permission_service.get_entities(session)


@router.post("/")
async def create_permission(permission: schemas.PermissionCreate, session: AsyncSession = Depends(get_async_session)):
    return await permission_service.create_entity(permission, session)


@router.get("/{permission_id}")
async def get_permission(permission_id: int, session: AsyncSession = Depends(get_async_session)):
    return await permission_service.get_entity(permission_id, session)


@router.patch("/{permission_id}")
async def update_permission(permission_id: int, permission: schemas.PermissionUpdate,
                        session: AsyncSession = Depends(get_async_session)):
    return await permission_service.update_entity(permission_id, permission, session)


@router.delete("/{permission_id}")
async def delete_permission(permission_id: int, session: AsyncSession = Depends(get_async_session)):
    return await permission_service.delete_entity(permission_id, session)
