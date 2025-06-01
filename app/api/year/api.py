from ninja import Router, Schema
from typing import List
from .models import Year
from uuid import UUID
from django.shortcuts import get_object_or_404
from ..month.api import post_month
from ..month.models import Month

api = Router()


class YearInSchema(Schema):
    year: str


class YearOutSchema(Schema):
    id: UUID
    year: str


# Get all years stored in database
@api.get("/", response=List[YearOutSchema])
def get_all_years(request):
    return Year.objects.all()


# Get year by id
@api.get("/{year_id}", response=YearOutSchema)
def get_year_by_id(request, year_id: UUID):
    year = get_object_or_404(Year, id=year_id)
    return year


# Post a year to the database
@api.post("/", response=YearOutSchema)
def post_year(request, payload: YearInSchema):
    return Year.objects.create(**payload.dict())


# Post a year and populate 12 months
@api.post("complete/", response=YearOutSchema)
def post_complete_year(request, payload: YearInSchema):
    year = Year.objects.create(**payload.dict())
    for month in [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]:
        Month.objects.create(**{"month": month, "year": year})
    return year


# Update a year by the id
@api.patch("/{year_id}", response=YearOutSchema)
def patch_year(request, year_id: UUID, payload: YearInSchema):
    year = get_object_or_404(Year, id=year_id)

    setattr(year, "year", payload.year)
    year.save()
    return year


# Delete a year by the id
@api.delete("/{year_id}")
def delete_year(request, year_id: UUID):
    year = get_object_or_404(Year, id=year_id)
    year.delete()
    return {"success": True}
