from fastapi import APIRouter, Depends, Query

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_bearer import JWTBearer
from src.auth.services import check_permission
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
async def get_categories(page: int = None,
                         limit: int = None,
                         search: str = None,
                         lang: str = Query(choices=["ru", "en", "uz"]),
                         session: AsyncSession = Depends(get_async_session),
                         current_user: str = Depends(JWTBearer())):
    check_permission("read_category", current_user)
    return await categories_service.get_entities(session, page, limit, search, lang)


@router.post("/")
async def create_category(category: schemas.CategoryCreate, session: AsyncSession = Depends(get_async_session),
                          current_user: str = Depends(JWTBearer())):
    check_permission("create_category", current_user)
    return await categories_service.create_entity(category, session)


@router.get("/{category_id}")
async def get_category(category_id: int, session: AsyncSession = Depends(get_async_session),
                       current_user: str = Depends(JWTBearer())):
    check_permission("read_category", current_user)
    return await categories_service.get_entity(category_id, session)


@router.patch("/{category_id}")
async def update_category(category_id: int, category: schemas.CategoryUpdate,
                          session: AsyncSession = Depends(get_async_session),
                          current_user: str = Depends(JWTBearer())):
    check_permission("update_category", current_user)
    return await categories_service.update_entity(category_id, category, session)


@router.delete("/")
async def delete_category(category_ids: list[int], session: AsyncSession = Depends(get_async_session),
                          current_user: str = Depends(JWTBearer())):
    check_permission("delete_category", current_user)
    return await categories_service.delete_entities(category_ids, session)
