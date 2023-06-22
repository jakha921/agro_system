from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException

from src.config import jwt_config

# Configuration
SECRET_KEY = jwt_config.SECRET_KEY
ALGORITHM = jwt_config.algorithm
ACCESS_TOKEN_EXPIRE = jwt_config.access_token_expire
REFRESH_TOKEN_EXPIRE = jwt_config.refresh_token_expire


# Function to create access token
def create_access_token(user_id: int) -> str:
    payload = {
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE),
        "user_id": user_id
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# Function to create refresh token
def create_refresh_token(user_id: int) -> str:
    payload = {
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE),
        "user_id": user_id
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# Function to decode JWT
def decode_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        return {}
