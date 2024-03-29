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
def create_access_token(user_id: int, is_admin: bool = False, role_id: int = None, permissions: list = None) -> str:
    if user_id == 1:
        payload = {
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE),
            "user_id": user_id,
            "permissions": [
                "read_admin",
                "create_admin",
                "update_admin",
                "delete_admin",
                "read_category",
                "create_category",
                "update_category",
                "delete_category",
                "read_guide",
                "create_guide",
                "update_guide",
                "delete_guide",
                "read_complain",
                "create_complain",
                "update_complain",
                "delete_complain",
                "read_department",
                "create_department",
                "update_department",
                "delete_department",
                "read_right",
                "create_right",
                "update_right",
                "delete_right",
                "read_role",
                "create_role",
                "update_role",
                "delete_role",
                "read_user",
                "create_user",
                "update_user",
                "delete_user",
            ]
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    if not is_admin:
        payload = {
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE),
            "user_id": user_id,
            "permissions": [
                "read_user",
                "update_user",
                "delete_user",
                "read_category",
                "read_right",
                "read_department",
                "read_guide",
                "create_complain",
                "read_complain",
                "update_complain",
                "delete_complain"
            ]
        }
    else:
        payload = {
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE),
            "admin_id": user_id,
            "role_id": role_id,
            "permissions": permissions
        }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# Function to decode JWT
def decode_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        return {}


# check permission
def check_permission(permission: str, current_user: str = Depends(decode_jwt)):
    if permission not in decode_jwt(current_user)['permissions']:
        raise HTTPException(status_code=403, detail={
            "status": "error",
            "message": "You don't have permission to access this resource",
            "data": None
        })
    return True
