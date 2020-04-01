from django.db import models
from django_extensions.db.models import TimeStampedModel


class Subscribe(TimeStampedModel):
    name = models.CharField(null=False, blank=False, max_length=255)
    email = models.EmailField(null=False, blank=False)

    def __str__(self):
        return f"{self.email}"
