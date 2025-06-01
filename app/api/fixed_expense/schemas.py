from ninja import Schema
from uuid import UUID
from datetime import date
from ..month.schemas import MonthSchema


class FixedExpense(Schema):
    id: UUID
    due: date
    budget: float
    actual: float
