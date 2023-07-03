from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_bearer import JWTBearer
from src.auth.services import check_permission
from src.database import get_async_session
from src.models import User
from src.users import schemas
from src.users.services import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    # responses={404: {"description": "Not found"}},
)
users_service = UserService(User)


@router.get("/")
async def get_users(page: int = None, limit: int = None, search: str = None,
                    session: AsyncSession = Depends(get_async_session),
                    current_user: str = Depends(JWTBearer())):
    check_permission("read_user", current_user)
    return await users_service.get_entities(session, page, limit, search)


@router.post("/")
async def create_user(user: schemas.UserCreate, session: AsyncSession = Depends(get_async_session),
                      current_user: str = Depends(JWTBearer())):
    check_permission("create_user", current_user)
    return await users_service.create_entity(user, session)


@router.get("/{user_id}")
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session),
                   current_user: str = Depends(JWTBearer())):
    check_permission("read_user", current_user)
    return await users_service.get_entity(user_id, session)


@router.patch("/{user_id}")
async def update_user(user_id: int, user: schemas.UserUpdate,
                      session: AsyncSession = Depends(get_async_session),
                      current_user: str = Depends(JWTBearer())):
    check_permission("update_user", current_user)
    return await users_service.update_entity(user_id, user, session)


@router.delete("/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session),
                      current_user: str = Depends(JWTBearer())):
    check_permission("delete_user", current_user)
    return await users_service.delete_entity(user_id, session)
