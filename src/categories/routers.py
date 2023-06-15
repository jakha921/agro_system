from fastapi import APIRouter, Depends
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models import Category
from src.categories import schemas
from src.categories.services import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    # responses={404: {"description": "Not found"}},
)
categories_service = CategoryService(Category)


@router.get("/")
async def get_categories(session: AsyncSession = Depends(get_async_session)):
    return await categories_service.get_entities(session)


@router.post("/")
async def create_category(category: schemas.CategoryCreate, session: AsyncSession = Depends(get_async_session)):
    return await categories_service.create_entity(category, session)


@router.get("/{category_id}")
async def get_category(category_id: int, session: AsyncSession = Depends(get_async_session)):
    return await categories_service.get_entity(category_id, session)


@router.patch("/{category_id}")
async def update_category(category_id: int, category: schemas.CategoryUpdate,
                          session: AsyncSession = Depends(get_async_session)):
    return await categories_service.update_entity(category_id, category, session)


@router.delete("/{category_id}")
async def delete_category(category_id: int, session: AsyncSession = Depends(get_async_session)):
    return await categories_service.delete_entity(category_id, session)
