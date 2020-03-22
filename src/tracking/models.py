from django.db import models
from django.utils.translation import gettext as _
from django_extensions.db.models import TimeStampedModel


UNKNOWN = "D"
SUSPECT = "S"
RECOVERED = "R"
CONFIRMED = "C"
NEGATIVATED = "N"


PERSON_STATUS_CHOICES = (
    (UNKNOWN, _("Desconhecido")),
    (SUSPECT, _("Suspeita de Corona Vírus")),
    (RECOVERED, _("Recuperado")),
    (CONFIRMED, _("Corona Vírus Confirmado")),
    (NEGATIVATED, _("Negativado")),
)


class Person(models.Model):
    age = models.PositiveIntegerField()
    status = models.CharField(
        choices=PERSON_STATUS_CHOICES, default=UNKNOWN, max_length=1
    )
    beacon_id = models.CharField(unique=True, max_length=36)

    def __str__(self):
        return f"{self.age}: {self.status}"


class PersonStatusChange(TimeStampedModel):
    person = models.ForeignKey(
        "tracking.Person", on_delete=models.CASCADE, related_name="person_status_change"
    )
    previous = models.CharField(
        choices=PERSON_STATUS_CHOICES, default=UNKNOWN, max_length=1
    )
    next = models.CharField(
        choices=PERSON_STATUS_CHOICES, default=UNKNOWN, max_length=1
    )
    health_professional = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, blank=True
    )

class PersonRiskFactor(TimeStampedModel):
    person = models.ForeignKey(
        "tracking.Person", on_delete=models.CASCADE, related_name="risk_factors"
    )
    risk_factor = models.ForeignKey(
        "tracking.RiskFactor", on_delete=models.CASCADE, related_name="persons"
    )

    class Meta:
        verbose_name_plural = "Person Risk Factors"

    def __str__(self):
        return f"{self.person}: {self.risk_factor}"


class RiskFactor(TimeStampedModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Risk Factors"

    def __str__(self):
        return self.name
