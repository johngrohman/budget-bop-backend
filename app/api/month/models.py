from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from ..year.models import Year
from ...db import UserOwnedModel

import uuid

class Month(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    month = models.CharField()
    date = models.DateField(null=True)
    year = models.ForeignKey(Year, null=True, on_delete=models.CASCADE)

    objects = UserOwnedModel()

    # Put function contents in util files to prevent circular import?
    @property
    def total_income(self) -> dict:
        from ..income.models import Income
        total_income_actual = Income.objects.filter(month=self.id).aggregate(Sum('actual'))['actual__sum']
        total_income_expected = Income.objects.filter(month=self.id).aggregate(Sum('expected'))['expected__sum']
        total_income_actual = 0.0 if total_income_actual is None else float(total_income_actual)
        total_income_expected = 0.0 if total_income_expected is None else float(total_income_expected)
        return {'expected': total_income_expected, 'actual': total_income_actual}
    
    @property
    def total_fixed_expenses(self) -> dict:
        from ..fixed_expense.models import FixedExpense
        total_fixed_expense_actual = FixedExpense.objects.filter(month=self.id).aggregate(Sum('actual'))['actual__sum']
        total_fixed_expense_actual = 0.0 if total_fixed_expense_actual is None else float(total_fixed_expense_actual)

        total_fixed_expense_budget = FixedExpense.objects.filter(month=self.id).aggregate(Sum('budget'))['budget__sum']
        total_fixed_expense_budget = 0.0 if total_fixed_expense_budget is None else float(total_fixed_expense_budget)
        return {'budget': total_fixed_expense_budget, 'actual': total_fixed_expense_actual}

    @property
    def total_variable_expenses(self) -> dict:
        from ..variable_expense.models import VariableExpense
        total_variable_expense_actual = VariableExpense.objects.filter(month=self.id).aggregate(Sum('actual'))['actual__sum']
        total_variable_expense_actual = 0.0 if total_variable_expense_actual is None else float(total_variable_expense_actual)

        total_variable_expense_budget = VariableExpense.objects.filter(month=self.id).aggregate(Sum('budget'))['budget__sum']
        total_variable_expense_budget = 0.0 if total_variable_expense_budget is None else float(total_variable_expense_budget)

        return {'budget': total_variable_expense_budget, 'actual': total_variable_expense_actual}

    @property
    def total_savings(self):
        from ..savings.models import Savings
        total_savings_actual = Savings.objects.filter(month=self.id).aggregate(Sum('actual'))['actual__sum']
        total_savings_actual = 0.0 if total_savings_actual is None else float(total_savings_actual)

        total_savings_budget = Savings.objects.filter(month=self.id).aggregate(Sum('budget'))['budget__sum']
        total_savings_budget = 0.0 if total_savings_budget is None else float(total_savings_budget)

        return {'budget': total_savings_budget, 'actual': total_savings_actual}

    class Meta:
        db_table = "Month"
