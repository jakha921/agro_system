from typing import Optional

from pydantic import BaseModel


class RoleCreate(BaseModel):
    name_ru: str
    name_en: Optional[str]
    name_uz: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name_ru": "Администратор",
                "name_en": "Administrator",
                "name_uz": "Administrator"
            }
        }
