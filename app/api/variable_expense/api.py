from ninja import Query, Router, Schema, FilterSchema
from typing import Optional, List, Dict
from ..month.schemas import MonthSchema
from uuid import UUID
from .models import VariableExpense
from django.shortcuts import get_object_or_404
from .utils import populate_variable_expenses
from .schemas import VariableExpenseInMonthSchema

api = Router()


class VariableExpenseFilterSchema(FilterSchema):
    name: Optional[str] = None
    budget: Optional[float] = None
    actual: Optional[float] = None
    month_id: Optional[UUID] = None


class VariableExpenseOutSchema(Schema):
    id: UUID
    name: Optional[str] = None
    budget: Optional[float] = None
    actual: Optional[float] = None
    month: Optional[MonthSchema] = None


class VariableExpenseInSchema(Schema):
    name: Optional[str] = None
    budget: Optional[float] = None
    actual: Optional[float] = None
    month_id: Optional[UUID] = None


@api.get("/", response=List[VariableExpenseOutSchema])
def list_variable_expense(request, filters: VariableExpenseFilterSchema = Query(...)):
    """
    List all variable expenses based on filters
    """
    filter_kwargs = filters.dict(exclude_unset=True)
    variable_expenses = VariableExpense.objects.filter(**filter_kwargs)
    return variable_expenses


@api.get(
    "/month/{month_id}",
    response=Dict[str, float],
    summary="Get Variable Expenses By Month ID",
)
def get_variable_expenses_in_month(request, month_id: UUID):
    """
    Retrieve a summary of transactions (variable expenses) in a given month.
    """
    result = populate_variable_expenses(month_id=month_id)
    return result


@api.post("/", response=VariableExpenseOutSchema)
def post_variable_expense(request, payload: VariableExpenseInSchema):
    return VariableExpense.objects.create(**payload.dict())


@api.patch("/{variable_expense_id}", response=VariableExpenseOutSchema)
def patch_variable_expense(
    request, variable_expense_id: UUID, payload: VariableExpenseInSchema
):
    variable_expense = get_object_or_404(VariableExpense, id=variable_expense_id)

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(variable_expense, attr, value)

    variable_expense.save()
    return variable_expense


@api.delete("/")
def delete_variable_expense(
    request, payload: list[UUID]
):
    for var_exp_id in payload:
        variable_expense = get_object_or_404(VariableExpense, id=var_exp_id)
        variable_expense.delete()
    return {"success": True}
