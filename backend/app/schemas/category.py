from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class CategoryResponse(BaseModel):
    id: int
    name: str
    type: str
    created_at: datetime
    is_active: bool


class CategoryCreate(BaseModel):
    name: str
    type: Literal["income", "expense", "transfer"]

class CategoryUpdate(BaseModel):
    name: str | None = None
    type: Literal["income", "expense", "transfer"] | None = None