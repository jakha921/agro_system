from typing import Optional

from pydantic import BaseModel, Field


class DepartmentCreate(BaseModel):
    title: str
    phone: str = Field(None, max_length=255)
    address: str = Field(None, max_length=255)
    district_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Toshkent shahar",
                "phone": "+998712000000",
                "address": "Toshkent shahar, Yunusobod tumani, Yunusobod ko'chasi, 1-uy",
                "district_id": 1
            }
        }


class DepartmentUpdate(DepartmentCreate):
    title: Optional[str]
    phone: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = Field(None, max_length=255)
    district_id: Optional[int]
