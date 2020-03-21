from django.db import models
from django_extensions.db.models import TimeStampedModel


class Rule(TimeStampedModel):
    name = models.CharField(
        max_length=255, null=False, blank=False, verbose_name="Nome"
    )

    message = models.CharField(
        max_length=255, null=False, blank=False, verbose_name="Mensagem"
    )
    enabled = models.BooleanField(null=False, default=True, blank=False)

    def __str__(self):
        return f"{self.name}"
