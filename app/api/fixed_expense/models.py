from django.db import models
from ..month.models import Month
import uuid

class FixedExpense(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField()
    due = models.DateField()
    budget = models.FloatField()
    actual = models.FloatField()
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