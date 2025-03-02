from django.db import models
from ..month.models import Month
import uuid

class Savings(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    budget = models.IntegerField()
    actual = models.FloatField()
    date = models.DateField()
    month = models.ForeignKey(Month, null=True, on_delete=models.CASCADE)