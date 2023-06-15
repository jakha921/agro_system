from typing import Optional

from pydantic import BaseModel


class CountryCreate(BaseModel):
    name_ru: str
    name_en: Optional[str]
    name_uz: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name_ru": "Узбекистан",
                "name_en": "Uzbekistan",
                "name_uz": "O'zbekiston"
            }
        }


class CountryUpdate(CountryCreate):
    name_ru: Optional[str]
