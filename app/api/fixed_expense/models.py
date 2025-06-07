from django.db import models
from ..month.models import Month
import uuid


class FixedExpense(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(null=True)
    date = models.DateField(null=True)
    budget = models.FloatField(null=True)
    actual = models.FloatField(null=True)
    month = models.ForeignKey(Month, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return {
            self.name,
            self.date,
            self.budget,
            self.actual,
            self.month,
        }

    class Meta:
        db_table = "Fixed_Expense"
