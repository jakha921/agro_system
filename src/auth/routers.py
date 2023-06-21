from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.services import get_current_user, create_access_token
from src.database import get_async_session
from src.users.routers import users_service

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    # responses={404: {"description": "Not found"}},
)


# Example login route
@router.post("/login")
async def login(phone_number: str, password: str, session: AsyncSession = Depends(get_async_session)):
    # Perform authentication and get the user_id
    user_id = await users_service.get_authenticate_user(phone_number, password, session)
    print('user_id', user_id)

    # Create the access token and refresh token
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)

    return {"access_token": access_token, "refresh_token": refresh_token}


# Example refresh route
@router.post("/refresh")
async def refresh(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Create a new access token
    new_access_token = create_access_token(user_id)

    return {"access_token": new_access_token}


# Example protected route
@router.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}! This is a protected route."}
