from ninja import Router
from typing import List
from .models import Year
from .schemas import YearSchema

router = Router()

@router.get('/', response=List[YearSchema])
def get_all_years(request):
    return Year.objects.all()

@router.post("/", response=YearSchema)
def post_year(request, payload: YearSchema):
    return Year.objects.create(**payload.dict())