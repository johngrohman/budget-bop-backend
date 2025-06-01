from ninja import Schema
from uuid import UUID
from datetime import date
from ..month.schemas import MonthSchema


class SavingsSchema(Schema):
    id: UUID
    name: str
    budget: int
    actual: float
    date: date
    month: MonthSchema
