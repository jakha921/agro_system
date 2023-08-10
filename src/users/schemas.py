from typing import Optional

from pydantic import BaseModel, Field
from pydantic.schema import Enum


class DeviceType(str, Enum):
    android = 'android'
    ios = 'ios'


class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    phone_number: str = Field(..., max_length=50)
    password: str = Field(..., max_length=50)
    age: int = Field(..., gt=0)
    address: str = Field(None, max_length=255)
    gender_id: int = Field(..., gt=0)
    status_id: int = Field(..., gt=0)
    city_id: int = Field(..., gt=0)
    district_id: Optional[int] = Field(None, gt=0)
    device_type: DeviceType = Field(DeviceType.android)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "user",
                "phone_number": "+998901234567",
                "password": "password",
                "age": 20,
                "address": "Tashkent",
                "gender_id": 1,
                "status_id": 1,
                "city_id": 1,
                "district_id": 1
            }
        }


class UserUpdate(UserCreate):
    # set all fields as optional
    username: Optional[str] = Field(None, max_length=50)
    phone_number: Optional[str] = Field(None, max_length=50)
    password: Optional[str] = Field(None, max_length=50)
    age: Optional[int] = Field(None, gt=0)
    address: Optional[str] = Field(None, max_length=255)
    city_id: Optional[int] = Field(None, gt=0)
