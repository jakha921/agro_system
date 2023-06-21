from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from src.config import jwt_config

# Configuration
SECRET_KEY = jwt_config.SECRET_KEY
ALGORITHM = jwt_config.algorithm
ACCESS_TOKEN_EXPIRE = jwt_config.access_token_expire
REFRESH_TOKEN_EXPIRE = jwt_config.refresh_token_expire

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# Function to create access token
def create_access_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE)
    to_encode = {"sub": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to create refresh token
def create_refresh_token(user_id: str) -> str:
    expires_delta = REFRESH_TOKEN_EXPIRE
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": user_id, "exp": expire}
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to verify and decode JWT token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id
