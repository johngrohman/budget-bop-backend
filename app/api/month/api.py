from ninja import Query, Router, Schema, FilterSchema
from typing import List, Optional
from .models import Month
from .schemas import MonthIncome, MonthVariableExpense, MonthFixedExpense, MonthSavings
from ..year.schemas import YearSchema
from ..year.models import Year
from uuid import UUID
from django.shortcuts import get_object_or_404

api = Router()


class MonthInSchema(Schema):
    month: str
    year: UUID


class MonthOutSchema(Schema):
    id: UUID
    month: str
    year: YearSchema
    total_income: Optional[MonthIncome] = None
    total_fixed_expenses: Optional[MonthFixedExpense] = None
    total_variable_expenses: Optional[MonthVariableExpense] = None
    total_savings: Optional[MonthSavings] = None


class MonthFilterSchema(FilterSchema):
    year_id: Optional[UUID] = None


# Get all months stored in database
# @api.get('/', response=List[MonthOutSchema])
# def get_all_months(request):
#     return Month.objects.all()


# Get month by id
@api.get("/{month_id}", response=MonthOutSchema)
def get_month_by_id(request, month_id: UUID):
    month = get_object_or_404(Month, id=month_id)
    return month


# Create a month
@api.post("", response=MonthOutSchema)
def post_month(request, payload: MonthInSchema):
    year = get_object_or_404(Year, id=payload.year)
    result = {"month": payload.month, "year": year, "user": request.user}
    return Month.objects.create(**result)


# Update a month by the id
@api.patch("/{month_id}", response=MonthOutSchema)
def patch_month(request, month_id: UUID, payload: MonthInSchema):
    month = get_object_or_404(Month, id=month_id)
    setattr(month, "month", payload.month)
    setattr(month, "year", payload.year)
    month.save()
    return month


# Delete a month by the id
@api.delete("/{month_id}")
def delete_month(request, month_id: UUID):
    month = get_object_or_404(Month, id=month_id)
    month.delete()
    return {"success": True}


@api.get("year/{year_id}", response=List[MonthOutSchema])
def list_months_in_year(request, year_id: UUID):
    months = Month.objects.filter(year__id=year_id).order_by('date')
    return months if months.exists() else []
