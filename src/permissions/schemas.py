from typing import Optional

from pydantic import BaseModel


class PermissionCreate(BaseModel):
    name_ru: str
    name_en: Optional[str]
    name_uz: Optional[str]
    description: Optional[str]
    role_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name_ru": "Просмотр",
                "name_en": "View",
                "name_uz": "Ko'rish",
                "description": "Просмотр информации",
                "role_id": 1
            }
        }


class PermissionUpdate(PermissionCreate):
    name_ru: Optional[str]
