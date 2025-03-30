from ninja import Query, Router, Schema, FilterSchema
from typing import Optional, List
from datetime import datetime
from datetime import date as dateType
from ..month.schemas import MonthSchema
from uuid import UUID
from .models import FixedExpense
from django.shortcuts import get_object_or_404

api = Router()

class FixedExpenseFilterSchema(FilterSchema):
    name: Optional[str] = None
    due: Optional[datetime] = None
    budget: Optional[float] = None
    actual: Optional[float] = None
    month_id: Optional[UUID] = None

class FixedExpenseOutSchema(Schema):
    id: UUID
    name: str
    due: dateType
    budget: float
    actual: float
    month: MonthSchema

class FixedExpenseInSchema(Schema):
    name: Optional[str] = None
    due: Optional[dateType] = None
    budget: Optional[float] = None
    actual: Optional[float] = None
    month_id: Optional[UUID] = None

@api.get('/', response=List[FixedExpenseOutSchema])
def list_fixed_expense(request, filters: FixedExpenseFilterSchema = Query(...)):
    """
    List all fixed expenses based on filters
    """
    fixed_expenses = FixedExpense.objects.all()
    fixed_expenses = filters.filter(fixed_expenses)
    return fixed_expenses

@api.post('/', response=FixedExpenseOutSchema)
def post_fixed_expense(request, payload: FixedExpenseInSchema):
    return FixedExpense.objects.create(**payload.dict())

@api.patch('/{fixed_expense_id}', response=FixedExpenseOutSchema)
def patch_fixed_expense(request, fixed_expense_id: UUID, payload: FixedExpenseInSchema):
    fixed_expense = get_object_or_404(FixedExpense, id=fixed_expense_id)

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(fixed_expense, attr, value)

    fixed_expense.save()
    return fixed_expense

@api.delete('/{fixed_expense_id}')
def delete_fixed_expense(request, fixed_expense_id: UUID):
    fixed_expense = get_object_or_404(FixedExpense, id=fixed_expense_id)
    fixed_expense.delete()
    return{"success": True}
