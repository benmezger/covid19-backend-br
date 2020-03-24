from django.db import models
from django_extensions.db.models import TimeStampedModel


# Temporary class
class Rule(TimeStampedModel):
    title = models.CharField(max_length=255)
    message = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Notification(TimeStampedModel):
    rule = models.ForeignKey(
        "notification.Rule",
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
        return self.rule.title

    @property
    def message(self):
        return self.rule.message
