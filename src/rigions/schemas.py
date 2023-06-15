from typing import Optional

from pydantic import BaseModel


class RegionCreate(BaseModel):
    country_id: int
    name_ru: str
    name_en: Optional[str]
    name_uz: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "country_id": 1,
                "name_ru": "Ташкент",
                "name_en": "Tashkent",
                "name_uz": "Toshkent"
            }
        }


class RegionUpdate(RegionCreate):
    country_id: Optional[int]
    name_ru: Optional[str]