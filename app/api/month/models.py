from django.db import models
import uuid

class Month(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    month = models.CharField()
    year = models.ForeignKey("year", null=True)