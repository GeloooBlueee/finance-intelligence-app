from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class AccountResponse(BaseModel):
    id: int
    name: str
    type: str
    initial_balance: Decimal
    is_active: bool
    created_at: datetime

class AccountCreate(BaseModel):
    name: str
    type: Literal["bank", "e-wallet", "cash", "credit_card", "investment"]
    initial_balance: Decimal = Field(ge=0)

class AccountUpdate(BaseModel):
    name: str | None = None
    type: Literal["bank", "e-wallet", "cash", "credit_card", "investment"] | None = None
    initial_balance: Decimal | None = Field(default=None, ge=0)
