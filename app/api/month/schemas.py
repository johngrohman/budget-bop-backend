from ninja import Schema
from uuid import UUID
from ..year.schemas import YearSchema

class MonthSchema(Schema):
    id: UUID
    month: str
    year: YearSchema