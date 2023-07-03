from fastapi import APIRouter, Depends
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_bearer import JWTBearer
from src.auth.services import check_permission
from src.database import get_async_session
from src.models import City
from src.cities import schemas
from src.cities.services import CityService

router = APIRouter(
    prefix="/cities",
    tags=["city"],
    # responses={404: {"description": "Not found"}},
)
city_service = CityService(City)


@router.get("/")
async def get_cities(page: int = None, per_page: int = None, search: str = None,
                     session: AsyncSession = Depends(get_async_session),
                     current_user: str = Depends(JWTBearer())):
    check_permission("read_guide", current_user)
    return await city_service.get_entities(session, page, per_page, search)


@router.post("/")
async def create_city(city: schemas.CityCreate, session: AsyncSession = Depends(get_async_session),
                      current_user: str = Depends(JWTBearer())):
    check_permission("create_guide", current_user)
    return await city_service.create_entity(city, session)


@router.get("/{city_id}")
async def get_city(city_id: int, session: AsyncSession = Depends(get_async_session),
                   current_user: str = Depends(JWTBearer())):
    check_permission("read_guide", current_user)
    return await city_service.get_entity(city_id, session)


@router.patch("/{city_id}")
async def update_city(city_id: int, city: schemas.CityUpdate,
                      session: AsyncSession = Depends(get_async_session),
                      current_user: str = Depends(JWTBearer())):
    check_permission("update_guide", current_user)
    return await city_service.update_entity(city_id, city, session)


@router.delete("/")
async def delete_city(city_ids: list[int], session: AsyncSession = Depends(get_async_session),
                      current_user: str = Depends(JWTBearer())):
    check_permission("delete_guide", current_user)
    return await city_service.delete_entities(city_ids, session)
