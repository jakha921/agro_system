from fastapi import APIRouter, Depends
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models import Admin
from src.admins import schemas
from src.admins.services import AdminService

router = APIRouter(
    prefix="/admins",
    tags=["admins"],
    # responses={404: {"description": "Not found"}},
)
admins_service = AdminService(Admin)


@router.get("/")
async def get_admins(page: int = None, limit: int = None, search: str = None,
                     session: AsyncSession = Depends(get_async_session)):
    return await admins_service.get_entities(session, page, limit, search)


@router.post("/")
async def create_admin(admin: schemas.AdminCreate, session: AsyncSession = Depends(get_async_session)):
    return await admins_service.create_entity(admin, session)


@router.get("/{admin_id}")
async def get_admin(admin_id: int, session: AsyncSession = Depends(get_async_session)):
    return await admins_service.get_entity(admin_id, session)


@router.patch("/{admin_id}")
async def update_admin(admin_id: int, admin: schemas.AdminUpdate,
                       session: AsyncSession = Depends(get_async_session)):
    return await admins_service.update_entity(admin_id, admin, session)


@router.delete("/{admin_id}")
async def delete_admin(admin_id: int, session: AsyncSession = Depends(get_async_session)):
    return await admins_service.delete_entity(admin_id, session)
