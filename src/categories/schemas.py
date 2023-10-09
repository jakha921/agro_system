from typing import Optional

from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    title_ru: str = Field(..., max_length=255)
    title_en: Optional[str] = Field(None, max_length=255)
    title_uz: Optional[str] = Field(None, max_length=255)
    short_description_ru: str = Field(..., max_length=255)
    short_description_en: Optional[str] = Field(None, max_length=255)
    short_description_uz: Optional[str] = Field(None, max_length=255)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title_ru": "Категория 1",
                "title_en": "Category 1",
                "title_uz": "Kategoriya 1",
                "short_description_ru": "Краткое описание категории 1",
                "short_description_en": "Short description of category 1",
                "short_description_uz": "Kategoriya 1ning qisqa ta'rif",
            }
        }


class CategoryUpdate(CategoryCreate):
    title_ru: Optional[str] = Field(None, max_length=255)
    short_description_ru: Optional[str] = Field(None, max_length=255)
