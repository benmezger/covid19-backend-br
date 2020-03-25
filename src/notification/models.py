from django.db import models
from django_extensions.db.models import TimeStampedModel


class Notification(TimeStampedModel):
    rule = models.ForeignKey(
        "rules.Rule",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="triggered_notifications",
    )
    person = models.ForeignKey(
        "tracking.Person",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notifications",
    )
    read = models.BooleanField(default=False)
    delivered = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.pk}"

    @property
    def title(self):
        return self.rule.name

    @property
    def message(self):
        return self.rule.message
