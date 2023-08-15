from fastapi import APIRouter, Depends
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_bearer import JWTBearer
from src.database import get_async_session
from src.models import Status
from src.statuses import schemas
from src.statuses.services import StatusService

router = APIRouter(
    prefix="/statuses",
    tags=["statuses"],
    # responses={404: {"description": "Not found"}},
)
status_service = StatusService(Status)


@router.get("/")
async def get_statuses(session: AsyncSession = Depends(get_async_session),
                       # current_user: str = Depends(JWTBearer())
                       ):
    return await status_service.get_entities(session)


@router.post("/")
async def create_status(status: schemas.StatusCreate, session: AsyncSession = Depends(get_async_session),
                        current_user: str = Depends(JWTBearer())):
    return await status_service.create_entity(status, session)


@router.get("/{status_id}")
async def get_status(status_id: int, session: AsyncSession = Depends(get_async_session),
                     current_user: str = Depends(JWTBearer())):
    return await status_service.get_entity(status_id, session)


@router.patch("/{status_id}")
async def update_status(status_id: int, status: schemas.StatusUpdate,
                        session: AsyncSession = Depends(get_async_session),
                        current_user: str = Depends(JWTBearer())):
    return await status_service.update_entity(status_id, status, session)


@router.delete("/")
async def delete_status(status_ids: list[int], session: AsyncSession = Depends(get_async_session),
                        current_user: str = Depends(JWTBearer())):
    return await status_service.delete_entities(status_ids, session)
