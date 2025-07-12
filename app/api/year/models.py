from django.db import models
from django.contrib.auth.models import User
import uuid


class Year(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    year = models.CharField(max_length=4)

    def __str__(self):
        return self.year

    class Meta:
        db_table = "Year"
