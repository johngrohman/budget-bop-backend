from ninja import Query, Router, Schema, FilterSchema
from typing import Optional, List
from ..month.schemas import MonthSchema
from uuid import UUID
from .models import VariableExpense
from django.shortcuts import get_object_or_404

api = Router()

class VariableExpenseFilterSchema(FilterSchema):
    name: Optional[str] = None
    budget: Optional[float] = None
    actual: Optional[float] = None
    month_id: Optional[UUID] = None

class VariableExpenseOutSchema(Schema):
    id: UUID
    name: str
    budget: float
    actual: float
    month: MonthSchema

class VariableExpenseInSchema(Schema):
    name: Optional[str] = None
    budget: Optional[float] = None
    actual: Optional[float] = None
    month_id: Optional[UUID] = None

@api.get('/', response=List[VariableExpenseOutSchema])
def list_variable_expense(request, filters: VariableExpenseFilterSchema = Query(...)):
    """
    List all variable expenses based on filters
    """
    variable_expenses = VariableExpense.objects.all()
    variable_expenses = filters.filter(variable_expenses)
    return variable_expenses

@api.post('/', response=VariableExpenseOutSchema)
def post_variable_expense(request, payload: VariableExpenseInSchema):
    return VariableExpense.objects.create(**payload.dict())

@api.patch('/{variable_expense_id}', response=VariableExpenseOutSchema)
def patch_variable_expense(request, variable_expense_id: UUID, payload: VariableExpenseInSchema):
    variable_expense = get_object_or_404(VariableExpense, id=variable_expense_id)

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(variable_expense, attr, value)

    variable_expense.save()
    return variable_expense

@api.delete('/{variable_expense_id}')
def delete_variable_expense(request, variable_expense_id: UUID):
    variable_expense = get_object_or_404(VariableExpense, id=variable_expense_id)
    variable_expense.delete()
    return{"success": True}
