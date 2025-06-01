from django.db import models
from ..month.models import Month
import uuid


class Income(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField()
    date = models.DateField()
    expected = models.FloatField()
    actual = models.FloatField()
    month = models.ForeignKey(Month, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return {self.name, self.date, self.expected, self.actual, self.month}

    class Meta:
        db_table = "Income"
