from typing import Optional

from pydantic import BaseModel


class DistrictCreate(BaseModel):
    city_id: int
    name_ru: str
    name_en: Optional[str]
    name_uz: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "city_id": 1,
                "name_ru": "Ташкент",
                "name_en": "Tashkent",
                "name_uz": "Toshkent"
            }
        }


class DistrictUpdate(DistrictCreate):
    city_id: Optional[int]
    name_ru: Optional[str]
