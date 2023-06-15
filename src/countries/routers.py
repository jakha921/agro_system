from fastapi import APIRouter, Depends
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models import Country
from src.countries import schemas
from src.countries.services import CountryService

router = APIRouter(
    prefix="/countries",
    tags=["countries"],
    # responses={404: {"description": "Not found"}},
)

country_service = CountryService(Country)


@router.get("/")
async def get_countries(session: AsyncSession = Depends(get_async_session)):
    return await country_service.get_entities(session)


@router.post("/")
async def create_country(country: schemas.CountryCreate, session: AsyncSession = Depends(get_async_session)):
    return await country_service.create_entity(country, session)


@router.get("/{country_id}")
async def get_country(country_id: int, session: AsyncSession = Depends(get_async_session)):
    return await country_service.get_entity(country_id, session)


@router.patch("/{country_id}")
async def update_country(country_id: int, country: schemas.CountryUpdate,
                         session: AsyncSession = Depends(get_async_session)):
    return await country_service.update_entity(country_id, country, session)


@router.delete("/{country_id}")
async def delete_country(country_id: int, session: AsyncSession = Depends(get_async_session)):
    return await country_service.delete_entity(country_id, session)


@router.get("/name/{country_name}")
async def get_country_by_name(country_name: str, session: AsyncSession = Depends(get_async_session)):
    return await country_service.get_country_by_name(country_name, session)
