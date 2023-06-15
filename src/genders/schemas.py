from typing import Optional

from pydantic import BaseModel


class GenderCreate(BaseModel):
    name_ru: str
    name_en: Optional[str]
    name_uz: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name_ru": "Мужской",
                "name_en": "Male",
                "name_uz": "Erkak"
            }
        }


class GenderUpdate(GenderCreate):
    name_ru: Optional[str]
