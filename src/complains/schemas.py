from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ComplainCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    complain_status_id: int = Field(..., gt=0)
    title: str = Field(..., max_length=50, min_length=3)
    description: str = Field(..., max_length=255)
    image: list[str] = Field(...)
    rate: int = Field(..., ge=0, le=4)
    action_date: datetime = Field(...)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "user_id": 1,
                "complain_status_id": 1,
                "title": "title",
                "description": "description",
                "image": ["image1", "image2"],
                "rate": 3,
                "action_date": "2021-07-05T14:08:15"
            }
        }


class ComplainUpdate(ComplainCreate):
    user_id: Optional[int] = Field(None, gt=0)
    complain_status_id: Optional[int] = Field(None, gt=0)
    title: Optional[str] = Field(None, max_length=50, min_length=3)
    description: Optional[str] = Field(None, max_length=255)
    image: Optional[str] = Field(None)
    rate: Optional[int] = Field(None, ge=0, lt=5)
    action_date: Optional[datetime] = Field(None)
