from typing import Optional

from pydantic import BaseModel


class CityCreate(BaseModel):
    region_id: int
    name_ru: str
    name_en: Optional[str]
    name_uz: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "region_id": 1,
                "name_ru": "Ташкент",
                "name_en": "Tashkent",
                "name_uz": "Toshkent"
            }
        }


class CityUpdate(CityCreate):
    region_id: Optional[int]
    name_ru: Optional[str]