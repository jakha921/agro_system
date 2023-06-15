from typing import Optional

from pydantic import BaseModel


class StatusCreate(BaseModel):
    name_ru: str
    name_en: Optional[str]
    name_uz: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name_ru": "Активный",
                "name_en": "Active",
                "name_uz": "Faol"
            }
        }


class StatusUpdate(StatusCreate):
    name_ru: Optional[str]
