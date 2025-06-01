from django.db.models import Sum
from uuid import UUID
from ..transaction.models import Transaction


def populate_variable_expenses(month_id: UUID):
    """
    Returns the sum of transactions per category and adds each entry to database.
    """
    transactions = (
        Transaction.objects.filter(month_id=month_id)
        .values("category")
        .annotate(total=Sum("amount"))
    )

    result = {entry["category"]: entry["total"] for entry in transactions}

    return result
