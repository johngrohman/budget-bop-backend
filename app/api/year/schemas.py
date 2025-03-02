from ninja import Schema
from uuid import UUID

class YearSchema(Schema):
    id: UUID
    year: str