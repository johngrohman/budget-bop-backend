from django.db import models
from django.contrib.auth.models import User
from ..month.models import Month
from ..year.models import Year
import uuid
from ...db import UserOwnedModel

class Transaction(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    date = models.DateField()
    amount = models.FloatField()
    description = models.CharField()
    category = models.CharField()
    month = models.ForeignKey(Month, null=True, on_delete=models.CASCADE)

    objects = UserOwnedModel()

    def __str__(self):
        return {self.date, self.amount, self.description, self.category, self.month}

    class Meta:
        db_table = "Transaction"
