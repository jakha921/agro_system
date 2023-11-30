from fastapi import Depends, APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.services import create_access_token
from src.database import get_async_session
from src.roles.services import RoleService
from src.users.routers import users_service
from src.admins.routers import admins_service

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    # responses={404: {"description": "Not found"}},
)


# Example login route
@router.post("/login")
async def login(phone_number: str, password: str, session: AsyncSession = Depends(get_async_session)):
    # Perform authentication and get the user_id
    user = await users_service.get_authenticate_user(phone_number, password, session)
    print('user', user)
    print('user', user['data'].id)

    # Create the access token and refresh token
    access_token = create_access_token(user['data'].id, False)

    return {"access_token": access_token, 'user': {
        "id": user['data'].id,
        "name": user['data'].username,
        "phone_number": user['data'].phone_number
    }}


# Example login route for admin
@router.post("/admin/login")
async def admin_login(email: str, password: str, session: AsyncSession = Depends(get_async_session)):
    # Perform authentication and get the user_id
    admin = await admins_service.get_authenticate_admin(email, password, session)
    print('admin token data', admin)
    role = await RoleService.get_role(admin['data'].role_id, session)
    get_role_permissions = await RoleService.get_role_permissions(admin['data'].role_id, session)

    # Create the access token and refresh token
    access_token = create_access_token(admin['data'].id, True, admin['data'].role_id, get_role_permissions)
    data = {
        "id": admin['data'].id,
        "name": admin['data'].username,
        "email": admin['data'].email,
        "role": role['data'],
    }

    return {"access_token": access_token, "data": data}


@router.get("/user/phone")
async def get_phone_number(phone_number: str, lang: str = None, session: AsyncSession = Depends(get_async_session)):
    is_exist_phone = await users_service.is_exist_phone(phone_number, session)
    if is_exist_phone:
        is_registered = True
        if lang == 'ru':
            msg = "Пользователь с таким номером телефона уже существует"
        elif lang == 'en':
            msg = "User with this phone number already exists"
        else:
            msg = "Foydalanuvchi bunday telefon raqami bilan mavjud"
    else:
        is_registered = False
        if lang == 'ru':
            msg = "Пользователь с таким номером телефона не существует"
        elif lang == 'en':
            msg = "User with this phone number does not exist"
        else:
            msg = "Foydalanuvchi bunday telefon raqami mavjud emas"

    return {"is_registered": is_registered, "message": msg}

# Example protected route
# @router.get("/protected")
# async def protected_route(
#         current_user: str = Depends(JWTBearer())):
#     check_permission("read_guide", current_user)
#     return {
#         "status": "success",
#         "message": "You have access to this resource",
#         "data": decode_jwt(current_user)
#     }
