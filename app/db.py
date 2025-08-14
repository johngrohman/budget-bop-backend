from django.db import models
from .middleware import get_current_user

class UserOwnedModel(models.Manager):
    def get_queryset(self):
        user = get_current_user()
        qs = super().get_queryset()
        if user and not user.is_superuser:
            qs = qs.filter(user_id=user.id)
        return qs
