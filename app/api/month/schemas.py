from ninja import Schema
from typing import Optional
from uuid import UUID
from ..year.schemas import YearSchema

class MonthIncome(Schema):
    expected: float
    actual: float

class MonthFixedExpense(Schema):
    budget: float
    actual: float

class MonthVariableExpense(Schema):
    budget: float
    actual: float

class MonthSavings(Schema):
    budget: float
    actual: float

class MonthSchema(Schema):
    id: UUID
    month: str
    year: YearSchema
    total_income: Optional[MonthIncome] = None
    total_fixed_expenses: Optional[MonthFixedExpense] = None
    total_variable_expenses: Optional[MonthVariableExpense] = None
    total_savings: Optional[MonthSavings] = None
 