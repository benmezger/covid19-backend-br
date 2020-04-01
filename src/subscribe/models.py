from django.db import models
from django_extensions.db.models import TimeStampedModel


class Subscribe(TimeStampedModel):
    email = models.EmailField(null=False, blank=False)

    def __str__(self):
        return f"{self.email}"
