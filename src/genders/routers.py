from fastapi import APIRouter, Depends
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_bearer import JWTBearer
from src.database import get_async_session
from src.models import Gender
from src.genders import schemas
from src.genders.services import GenderService

router = APIRouter(
    prefix="/genders",
    tags=["genders"],
    # responses={404: {"description": "Not found"}},
)
gender_service = GenderService(Gender)


@router.get("/")
async def get_genders(session: AsyncSession = Depends(get_async_session)):
    return await gender_service.get_entities(session)


@router.post("/")
async def create_gender(gender: schemas.GenderCreate, session: AsyncSession = Depends(get_async_session),
                        current_user: str = Depends(JWTBearer())):
    return await gender_service.create_entity(gender, session)


@router.get("/{gender_id}")
async def get_gender(gender_id: int, session: AsyncSession = Depends(get_async_session),
                     current_user: str = Depends(JWTBearer())):
    return await gender_service.get_entity(gender_id, session)


@router.patch("/{gender_id}")
async def update_gender(gender_id: int, gender: schemas.GenderUpdate,
                        session: AsyncSession = Depends(get_async_session),
                        current_user: str = Depends(JWTBearer())):
    return await gender_service.update_entity(gender_id, gender, session)


@router.delete("/{gender_id}")
async def delete_gender(gender_id: int, session: AsyncSession = Depends(get_async_session),
                        current_user: str = Depends(JWTBearer())):
    return await gender_service.delete_entity(gender_id, session)
