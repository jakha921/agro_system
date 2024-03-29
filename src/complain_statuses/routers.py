from fastapi import APIRouter, Depends
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_bearer import JWTBearer
from src.database import get_async_session
from src.models import ComplainStatus
from src.complain_statuses import schemas
from src.complain_statuses.services import ComplainStatusService

router = APIRouter(
    prefix="/complain_statuses",
    tags=["complain_statuses"],
    # responses={404: {"description": "Not found"}},
)
complain_status_service = ComplainStatusService(ComplainStatus)


@router.get("/")
async def get_complain_statuses(session: AsyncSession = Depends(get_async_session),
                                lang: str = None,
                                current_user: str = Depends(JWTBearer())):
    return await complain_status_service.get_entities(session, lang=lang)


@router.post("/")
async def create_complain_status(status: schemas.ComplainStatusCreate,
                                 session: AsyncSession = Depends(get_async_session),
                                 current_user: str = Depends(JWTBearer())):
    return await complain_status_service.create_entity(status, session)


@router.get("/{complain_statuses_id}")
async def get_status(complain_statuses_id: int, session: AsyncSession = Depends(get_async_session),
                     current_user: str = Depends(JWTBearer())):
    return await complain_status_service.get_entity(complain_statuses_id, session)


@router.patch("/{complain_statuses_id}")
async def update_complain_status(complain_statuses_id: int, status: schemas.ComplainStatusUpdate,
                                 session: AsyncSession = Depends(get_async_session),
                                 current_user: str = Depends(JWTBearer())):
    return await complain_status_service.update_entity(complain_statuses_id, status, session)


@router.delete("/{complain_statuses_id}")
async def delete_complain_status(complain_statuses_id: int, session: AsyncSession = Depends(get_async_session),
                                 current_user: str = Depends(JWTBearer())):
    return await complain_status_service.delete_entity(complain_statuses_id, session)
