from datetime import date as Date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    date: Date
    type: Literal["income", "expense", "transfer"]
    amount: Decimal
    description: str | None = None
    category_id: int | None = None
    account_id: int | None = None
    from_account_id: int | None = None
    to_account_id: int | None = None

class TransactionCreate(BaseModel):
    date: Date
    type: Literal["income", "expense", "transfer"]
    amount: Decimal = Field(gt=0)
    description: str | None = None
    category_id: int | None = None
    account_id: int | None = None
    from_account_id: int | None = None
    to_account_id: int | None = None

class TransactionUpdate(BaseModel):
    date: Date | None = None
    type: Literal["income", "expense", "transfer"] | None = None
    amount: Decimal | None = Field(default=None, gt=0)
    description: str | None = None
    category_id: int | None = None
    account_id: int | None = None
    from_account_id: int | None = None
    to_account_id: int | None = None