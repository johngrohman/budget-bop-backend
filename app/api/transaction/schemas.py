from ninja import Schema
from uuid import UUID
from datetime import date
from ..month.schemas import MonthSchema

class TransactionSchema(Schema):
    id: UUID
    date: date
    amount: float
    description: str
    category: str
    month_id: UUID