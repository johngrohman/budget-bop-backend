from django.db import models
from ..month.models import Month
import uuid
from django.contrib.auth.models import User


class Income(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(null=True)
    date = models.DateField(null=True)
    expected = models.FloatField(null=True)
    actual = models.FloatField(null=True)
    month = models.ForeignKey(Month, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return {self.name, self.date, self.expected, self.actual, self.month}

    class Meta:
        db_table = "Income"
