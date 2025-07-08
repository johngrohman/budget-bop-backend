from .models import Month
from ..income.models import Income
from ..fixed_expense.models import FixedExpense
from ..variable_expense.models import VariableExpense
from ..savings.models import Savings
from django.db.models import Sum

def month_sync_totals(month: Month) -> None:
    total_income = Income.objects.filter(month=month.id).aggregate(Sum('actual'))['actual__sum']
    total_income = 0 if total_income is None else float(total_income)

    total_fixed_expense = FixedExpense.objects.filter(month=month.id).aggregate(Sum('actual'))['actual__sum']
    total_fixed_expense = 0 if total_fixed_expense is None else float(total_fixed_expense)

    total_variable_expense = VariableExpense.objects.filter(month=month.id).aggregate(Sum('actual'))['actual__sum']
    total_variable_expense = 0 if total_variable_expense is None else float(total_variable_expense)

    total_savings = Savings.objects.filter(month=month.id).aggregate(Sum('actual'))['actual__sum']
    total_savings = 0 if total_savings is None else float(total_savings)

    total_spent = total_fixed_expense + total_variable_expense

    month.total_income = total_income
    month.total_spent = total_spent
    month.total_savings = total_savings
    month.save()