import sys, csv
from datetime import datetime
from collections import defaultdict
from uuid import UUID
from ..models import Transaction
from ...variable_expense.models import VariableExpense

def format_date(date_str):
    return datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")


def sync_vars_trans(month_id: UUID):
    """
    Iterates over transactions in a given month and **Creates** or **Updates** variable expenses

    Should be invoked every time a transaction is modified.
    """

    transactions = Transaction.objects.filter(month_id=month_id)

    variableExpensesCurr = defaultdict(float)

    for transaction in transactions:
        variableExpensesCurr[str(transaction.category)] += transaction.amount

    updateExpenses = []

    for category_str, amount in variableExpensesCurr.items():
        variableExpense, _ = VariableExpense.objects.get_or_create(
            month_id=month_id,
            name=category_str,
        )

        variableExpense.actual = amount
        variableExpense.save()

        updateExpenses.append({
            'id': str(variableExpense.id),
            'name': variableExpense.name,
            'budget': variableExpense.budget,
            'actual': variableExpense.actual,
            'month': str(variableExpense.month_id),
        })

    return updateExpenses