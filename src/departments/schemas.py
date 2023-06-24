from typing import Optional

from pydantic import BaseModel, Field


class DepartmentCreate(BaseModel):
    title_ru: str = Field(..., max_length=255)
    title_en: Optional[str] = Field(None, max_length=255)
    title_uz: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=255)
    phone_number: list[str] = Field(None, max_length=255)
    address: str = Field(None, max_length=255)
    district_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title_ru": "Халқ банки",
                "title_en": "People's Bank",
                "title_uz": "Xalq banki",
                "phone": "+998712000000",
                "phone_number": ["+998712000000", "+998712000001"],
                "address": "Toshkent shahar, Yunusobod tumani, Yunusobod ko'chasi, 1-uy",
                "district_id": 1
            }
        }


class DepartmentUpdate(DepartmentCreate):
    title_ru: Optional[str] = Field(None, max_length=255)
    title_en: Optional[str] = Field(None, max_length=255)
    title_uz: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=255)
    phone_number: list[str] = Field(None, max_length=255)
    address: Optional[str] = Field(None, max_length=255)
    district_id: Optional[int]
