from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ComplainCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    complain_status_id: int = Field(..., gt=0)
    title: str = Field(..., max_length=50, min_length=3)
    description: str = Field(..., max_length=255)
    image: str = Field(..., max_length=255)
    rate: int = Field(..., ge=0, le=5)
    action_date: datetime = Field(...)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "user_id": 1,
                "complain_status_id": 1,
                "title": "title",
                "description": "description",
                "image": "image",
                "rate": 5
            }
        }


class ComplainUpdate(ComplainCreate):
    user_id: Optional[int] = Field(None, gt=0)
    complain_status_id: Optional[int] = Field(None, gt=0)
    title: Optional[str] = Field(None, max_length=50, min_length=3)
    description: Optional[str] = Field(None, max_length=255)
    image: Optional[str] = Field(None)
    rate: Optional[int] = Field(None, ge=0, lt=5)
