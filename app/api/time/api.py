from ninja import Query, Router, Schema, FilterSchema
from typing import List, Optional
from ..month.models import Month
from ..year.schemas import YearSchema
from ..year.models import Year
from uuid import UUID
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

api = Router()


@api.get("years-months")
def list_all_time_data(request):
    years = Year.objects.all()
    data = []

    for year in years:
        months = Month.objects.filter(year__id=year.id).values()
        data.append(
            {"year": {"year": year.year, "id": year.id}, "months": list(months)}
        )

    return JsonResponse(data, safe=False)
