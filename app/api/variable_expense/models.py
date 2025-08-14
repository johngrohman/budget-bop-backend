from django.db import models
from django.contrib.auth.models import User
from ..month.models import Month
import uuid
from ...db import UserOwnedModel


class VariableExpense(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(null=True)
    budget = models.FloatField(null=True)
    actual = models.FloatField(null=True)
    month = models.ForeignKey(Month, null=True, on_delete=models.CASCADE)

    objects = UserOwnedModel()

    def __str__(self):
        return {
            self.name,
            self.budget,
            self.actual,
            self.month,
        }

    class Meta:
        db_table = "Variable_Expense"
