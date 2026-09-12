from datetime import date as Date
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.category import Category
from app.models.account import Account


class Transaction(Base):
    __tablename__ = "transactions"

    category: Mapped["Category"] = relationship("Category")
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[Date] = mapped_column(nullable=False)

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True
    )

    account_id: Mapped[int | None] = mapped_column(
        ForeignKey("accounts.id"),
        nullable=True
    )

    account: Mapped["Account"] = relationship(
        "Account",
        foreign_keys=[account_id]
    )

    from_account_id: Mapped[int | None] = mapped_column(
        ForeignKey("accounts.id"),
        nullable=True
    )

    from_account: Mapped["Account"] = relationship(
        "Account",
        foreign_keys=[from_account_id]
    )

    to_account_id: Mapped[int | None] = mapped_column(
        ForeignKey("accounts.id"),
        nullable=True
    )

    to_account: Mapped["Account"] = relationship(
        "Account",
        foreign_keys=[to_account_id]
    )