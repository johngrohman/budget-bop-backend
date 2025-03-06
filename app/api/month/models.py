from django.db import models
from ..year.models import Year
import uuid

class Month(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    month = models.CharField()
    year = models.ForeignKey(Year, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return (self.month, self.year.__str__)
    
    class Meta:
        db_table = "Month"