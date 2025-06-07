from ninja import Schema, FilterSchema
from uuid import UUID
from datetime import date as dateType
from ..month.schemas import MonthSchema
from typing import Optional


class SavingsSchema(Schema):
    id: UUID
    name: str
    budget: int
    actual: float
    date: dateType
    month: MonthSchema


class SavingsFilterSchema(FilterSchema):
    name: Optional[str] = None
    budget: Optional[str] = None
    actual: Optional[str] = None
    month_id: Optional[UUID] = None


class SavingsInSchema(Schema):
    name: Optional[str] = None
    budget: Optional[int] = None
    actual: Optional[float] = None
    date: Optional[dateType] = None
    month_id: Optional[UUID] = None


class SavingsOutSchema(Schema):
    id: UUID
    name: str
    budget: int
    actual: float
    date: dateType
    month: MonthSchema
