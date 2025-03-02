from ninja import Router, Schema
from typing import List
from .models import Savings
from ..month.schemas import MonthSchema
from ..month.models import Month
from uuid import UUID
from django.shortcuts import get_object_or_404
from datetime import date

api = Router()

class SavingsInSchema(Schema):
    name: str
    budget: int
    actual: float
    date: date
    month: str

class SavingsOutSchema(Schema):
    id: UUID
    name: str
    budget: int
    actual: float
    date: date
    month: MonthSchema

# Get all savings stored in database
@api.get('/', response=List[SavingsOutSchema])
def get_all_savings(request):
    return Savings.objects.all()

# Get savings by id
@api.get('/{savings_id}', response=SavingsOutSchema)
def get_savings_by_id(request, savings_id: UUID):
    savings = get_object_or_404(Savings, id=savings_id)
    return savings

# Create a savings object
@api.post('/', response=SavingsOutSchema)
def post_savings(request, payload: SavingsInSchema):
    # Ensure month exists
    month = get_object_or_404(Month, month=payload.month)
    result = {
        "name":payload.name,
        "budget":payload.budget,
        "actual":payload.actual,
        "date":payload.date,
        "month":month
    }
    return Savings.objects.create(**result)

# Update a savings object
# @api.patch('/{savings_id}', response=SavingsOutSchema)
# def patch_savings(request, savings_id: UUID, payload: SavingsInSchema):
#     pass

# Delete a savings by the id
@api.delete('/{savings_id}')
def delete_savings(request, savings_id: UUID):
    savings = get_object_or_404(Savings, id=savings_id)
    savings.delete()
    return {"success": True}