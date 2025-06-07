from ninja import Router, Schema, Query
from typing import List
from .models import Savings
from .schemas import (
    SavingsInSchema,
    SavingsOutSchema,
    SavingsFilterSchema,
)
from ..month.schemas import MonthSchema
from ..month.models import Month
from uuid import UUID
from django.shortcuts import get_object_or_404
from datetime import date

api = Router()


# Get all savings stored in database
@api.get("/", response=List[SavingsOutSchema])
def list_all_savings(request, filters: SavingsFilterSchema = Query(...)):
    """
    List all savings based on filters
    """
    filter_kwargs = filters.dict(exclude_unset=True)
    savings = Savings.objects.filter(**filter_kwargs)
    return savings


# Get savings by id
@api.get("/{savings_id}", response=SavingsOutSchema)
def get_savings_by_id(request, savings_id: UUID):
    savings = get_object_or_404(Savings, id=savings_id)
    return savings


# Create a savings object
@api.post("/", response=SavingsOutSchema)
def post_savings(request, payload: SavingsInSchema):
    return Savings.objects.create(**payload.dict())


# Update a savings object
@api.patch("/{savings_id}", response=SavingsOutSchema)
def patch_savings(request, savings_id: UUID, payload: SavingsInSchema):
    savings = get_object_or_404(Savings, id=savings_id)

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(savings, attr, value)

    savings.save()
    return savings


# Delete a savings by the id
@api.delete("/")
def delete_savings(request, payload: List[UUID]):
    for sav_id in payload:
        savings = get_object_or_404(Savings, id=sav_id)
        savings.delete()
    return {"success": True}
