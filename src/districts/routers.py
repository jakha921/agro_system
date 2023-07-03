from fastapi import APIRouter, Depends
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_bearer import JWTBearer
from src.auth.services import check_permission
from src.database import get_async_session
from src.models import District
from src.districts import schemas
from src.districts.services import DistrictService

router = APIRouter(
    prefix="/districts",
    tags=["districts"],
    # responses={404: {"description": "Not found"}},
)
district_service = DistrictService(District)


@router.get("/")
async def get_districts(page: int = None, per_page: int = None, search: str = None,
                        session: AsyncSession = Depends(get_async_session),
                        current_user: str = Depends(JWTBearer())):
    check_permission("read_guide", current_user)
    return await district_service.get_entities(session, page, per_page, search)


@router.post("/")
async def create_district(district: schemas.DistrictCreate, session: AsyncSession = Depends(get_async_session),
                          current_user: str = Depends(JWTBearer())):
    check_permission("create_guide", current_user)
    return await district_service.create_entity(district, session)


@router.get("/{district_id}")
async def get_district(district_id: int, session: AsyncSession = Depends(get_async_session),
                       current_user: str = Depends(JWTBearer())):
    check_permission("read_guide", current_user)
    return await district_service.get_entity(district_id, session)


@router.patch("/{district_id}")
async def update_district(district_id: int, district: schemas.DistrictUpdate,
                          session: AsyncSession = Depends(get_async_session),
                          current_user: str = Depends(JWTBearer())):
    check_permission("update_guide", current_user)
    return await district_service.update_entity(district_id, district, session)


@router.delete("/")
async def delete_district(district_ids: list[int], session: AsyncSession = Depends(get_async_session),
                          current_user: str = Depends(JWTBearer())):
    check_permission("delete_guide", current_user)
    return await district_service.delete_entities(district_ids, session)
