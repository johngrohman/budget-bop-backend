from ninja import Query, Router, Schema, FilterSchema
from typing import Optional, List
from datetime import datetime
from datetime import date as dateType
from ..month.schemas import MonthSchema
from uuid import UUID
from .models import Income
from django.shortcuts import get_object_or_404

api = Router()


class IncomeFilterSchema(FilterSchema):
    name: Optional[str] = None
    date: Optional[datetime] = None
    expected: Optional[float] = None
    actual: Optional[float] = None
    month_id: Optional[UUID] = None


class IncomeOutSchema(Schema):
    id: UUID
    name: str
    date: dateType
    expected: float
    actual: float
    month: MonthSchema


class IncomeInSchema(Schema):
    name: Optional[str] = None
    date: Optional[dateType] = None
    expected: Optional[float] = None
    actual: Optional[float] = None
    month_id: Optional[UUID] = None


@api.get("/", response=List[IncomeOutSchema])
def list_income(request, filters: IncomeFilterSchema = Query(...)):
    """
    Get a list of all income records.
    """
    income = Income.objects.all()
    income = filters.filter(income)
    return income


@api.post("/", response=IncomeOutSchema)
def post_income(request, payload: IncomeInSchema):
    return Income.objects.create(**payload.dict())


@api.patch("/{income_id}", response=IncomeOutSchema)
def patch_income(request, income_id: UUID, payload: IncomeInSchema):
    income = get_object_or_404(Income, id=income_id)

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(income, attr, value)

    income.save()
    return income


@api.delete("/{income_id}")
def delete_income(request, income_id: UUID):
    income = get_object_or_404(Income, id=income_id)
    income.delete()
    return {"success": True}
