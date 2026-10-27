from datetime import datetime

from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    text: str = Field(min_length=1)

class DocumentOut(BaseModel):
    id: str
    title: str
    created_at: datetime