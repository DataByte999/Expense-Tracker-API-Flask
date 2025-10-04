from pydantic import BaseModel, Field, field_serializer
from datetime import date
from decimal import Decimal
from typing import Annotated, Literal, Optional, List


class TransactionIn(BaseModel):
    kind: Literal["expense", "income"]
    transaction_date: date
    amount: Annotated[Decimal, Field(ge=0, decimal_places=2)]
    description: Annotated[str, Field(min_length=1, max_length=255)]

    # Add a field_serializer to the base model
    @field_serializer('transaction_date')
    def serialize_date_to_iso(self, d: date) -> str:
        return d.isoformat()



class TransactionOut(TransactionIn):
    id: Annotated[int, Field(ge=1)]



class TransactionsOut(BaseModel):
    transactions: List[TransactionOut]


class UpdateTransactionIn(BaseModel):
    kind: Optional[Literal["expense", "income"]] = None
    transaction_date: Optional[date] = None
    amount: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    description: Optional[str] = Field(None, min_length=1, max_length=255)


class TransactionId(BaseModel):
    id: Annotated[int, Field(ge=1)]


