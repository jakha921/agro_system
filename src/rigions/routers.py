from fastapi import APIRouter, Depends
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_bearer import JWTBearer
from src.auth.services import check_permission
from src.database import get_async_session
from src.models import Region
from src.rigions import schemas
from src.rigions.services import RegionService

router = APIRouter(
    prefix="/regions",
    tags=["regions"],
    # responses={404: {"description": "Not found"}},
)
region_service = RegionService(Region)


@router.get("/")
async def get_regions(page: int = None, per_page: int = None, search: str = None,
                      session: AsyncSession = Depends(get_async_session),
                      current_user: str = Depends(JWTBearer())):
    check_permission("read_guide", current_user)
    return await region_service.get_entities(session, page, per_page, search)


@router.post("/")
async def create_region(region: schemas.RegionCreate, session: AsyncSession = Depends(get_async_session),
                        current_user: str = Depends(JWTBearer())):
    check_permission("create_guide", current_user)
    return await region_service.create_entity(region, session)


@router.get("/{region_id}")
async def get_region(region_id: int, session: AsyncSession = Depends(get_async_session),
                     current_user: str = Depends(JWTBearer())):
    check_permission("read_guide", current_user)
    return await region_service.get_entity(region_id, session)


@router.patch("/{region_id}")
async def update_region(region_id: int, region: schemas.RegionUpdate,
                        session: AsyncSession = Depends(get_async_session),
                        current_user: str = Depends(JWTBearer())):
    check_permission("update_guide", current_user)
    return await region_service.update_entity(region_id, region, session)


@router.delete("/")
async def delete_region(region_ids: list[int], session: AsyncSession = Depends(get_async_session),
                        current_user: str = Depends(JWTBearer())):
    check_permission("delete_guide", current_user)
    return await region_service.delete_entities(region_ids, session)
