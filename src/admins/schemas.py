from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class AdminCreate(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., max_length=50)
    role_id: int = Field(..., gt=0)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "admin",
                "email": "user@example.com",
                "password": "12345678",
                "role_id": 1
            }
        }


class AdminUpdate(AdminCreate):
    # set all fields as optional
    username: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr]
    password: Optional[str] = Field(None, max_length=50)
    role_id: Optional[int] = Field(None, gt=0)
