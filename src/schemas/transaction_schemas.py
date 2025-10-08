from datetime import date
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, Field, field_serializer


class TransactionIn(BaseModel):
    kind: Literal["expense", "income"]
    transaction_date: date
    amount: Annotated[Decimal, Field(ge=0, decimal_places=2)]
    description: Annotated[str, Field(min_length=1, max_length=255)]

    # Add a field_serializer to the base model
    @field_serializer("transaction_date")
    def serialize_date_to_iso(self, d: date) -> str:
        return d.isoformat()


class TransactionOut(TransactionIn):
    id: Annotated[int, Field(ge=1)]


class TransactionsOut(BaseModel):
    transactions: list[TransactionOut]


class UpdateTransactionIn(BaseModel):
    kind: Literal["expense", "income"] | None = None
    transaction_date: date | None = None
    amount: Decimal | None = Field(None, ge=0, decimal_places=2)
    description: str | None = Field(None, min_length=1, max_length=255)


class TransactionId(BaseModel):
    id: Annotated[int, Field(ge=1)]
