from django.db import models
import uuid

class Year(models.Model):
    id_temp = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    year = models.CharField(max_length=4)

    def __str__(self):
        return self.year