from fastapi import APIRouter, Depends
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models import Complain
from src.complains import schemas
from src.complains.services import ComplainService

router = APIRouter(
    prefix="/complains",
    tags=["complains"],
    # responses={404: {"description": "Not found"}},
)
complains_service = ComplainService(Complain)


@router.get("/")
async def get_complains(page: int = None, limit: int = None, search: str = None,
                        session: AsyncSession = Depends(get_async_session)):
    return await complains_service.get_entities(session, page, limit, search)


@router.post("/")
async def create_complain(complain: schemas.ComplainCreate, session: AsyncSession = Depends(get_async_session)):
    return await complains_service.create_entity(complain, session)


@router.get("/{complain_id}")
async def get_complain(complain_id: int, session: AsyncSession = Depends(get_async_session)):
    return await complains_service.get_entity(complain_id, session)


@router.patch("/{complain_id}")
async def update_complain(complain_id: int, complain: schemas.ComplainUpdate,
                          session: AsyncSession = Depends(get_async_session)):
    return await complains_service.update_entity(complain_id, complain, session)


@router.delete("/{complain_id}")
async def delete_complain(complain_id: int, session: AsyncSession = Depends(get_async_session)):
    return await complains_service.delete_entity(complain_id, session)
