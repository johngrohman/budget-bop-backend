from ninja import Schema
from uuid import UUID
from datetime import date
from ..month.schemas import MonthSchema


class VariableExpense(Schema):
    id: UUID
    budget: float
    actual: float


class VariableExpenseInMonthSchema(Schema):
    category: str
    amount: float
