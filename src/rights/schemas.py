from typing import Optional

from pydantic import BaseModel, Field


class RightCreate(BaseModel):
    category_ids: list[int] = Field(..., min_items=1)
    title_ru: str = Field(..., max_length=255)
    title_en: Optional[str] = Field(None, max_length=255)
    title_uz: Optional[str] = Field(None, max_length=255)
    short_description_ru: str = Field(..., max_length=4000)
    short_description_en: Optional[str] = Field(None, max_length=4000)
    short_description_uz: Optional[str] = Field(None, max_length=4000)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "category_ids": [1, 2],
                "title_ru": "Право 1",
                "title_en": "Right 1",
                "title_uz": "Huquq 1",
                "short_description_ru": "Краткое описание по праву 1",
                "short_description_en": "Short description for right 1",
                "short_description_uz": "Huquq haqida qisqacha ma'lumot 1",
            }
        }


class RightUpdate(RightCreate):
    category_ids: Optional[list[int]] = Field(None, min_items=1)
    title_ru: Optional[str] = Field(None, max_length=255)
    short_description_ru: Optional[str] = Field(None, max_length=4000)
