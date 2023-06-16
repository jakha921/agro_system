from fastapi import APIRouter, Depends
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models import Right
from src.rights import schemas
from src.rights.services import RightService

router = APIRouter(
    prefix="/rights",
    tags=["rights"],
    # responses={404: {"description": "Not found"}},
)
rights_service = RightService(Right)


@router.get("/")
async def get_rights(session: AsyncSession = Depends(get_async_session)):
    return await rights_service.get_entities(session)


@router.post("/")
async def create_right(right: schemas.RightCreate, session: AsyncSession = Depends(get_async_session)):
    return await rights_service.create_entity(right, session)


@router.get("/{right_id}")
async def get_right(right_id: int, session: AsyncSession = Depends(get_async_session)):
    return await rights_service.get_entity(right_id, session)


@router.patch("/{right_id}")
async def update_right(right_id: int, right: schemas.RightUpdate,
                       session: AsyncSession = Depends(get_async_session)):
    return await rights_service.update_entity(right_id, right, session)


@router.delete("/{right_id}")
async def delete_right(right_id: int, session: AsyncSession = Depends(get_async_session)):
    return await rights_service.delete_entity(right_id, session)
