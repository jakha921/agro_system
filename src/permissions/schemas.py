from typing import Optional

from pydantic import BaseModel


class PermissionCreate(BaseModel):
    alias: str
    name_ru: Optional[str]
    name_en: Optional[str]
    name_uz: Optional[str]
    description: Optional[str]
    role_ids: list[int]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "alias": "create_guide",
                "name_ru": "Создание cправочника",
                "name_en": "Create guide",
                "name_uz": "Qo'llanma yaratish",
                "description": "Право на создание справочника",
                "role_ids": [1, 2]
            }
        }


class PermissionUpdate(PermissionCreate):
    pass
