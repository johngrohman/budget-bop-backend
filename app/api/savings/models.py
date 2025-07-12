from django.db import models
from ..month.models import Month
from django.contrib.auth.models import User
import uuid


class Savings(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100, null=True)
    budget = models.IntegerField(null=True)
    actual = models.FloatField(null=True)
    date = models.DateField(null=True)
    month = models.ForeignKey(Month, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return {self.name, self.budget, self.actual, self.date, self.month}

    class Meta:
        db_table = "Savings"
