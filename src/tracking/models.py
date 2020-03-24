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
        return f"Age: {self.age} - Status: {self.get_status_display()}"


class PersonStatusChange(TimeStampedModel):
    person = models.ForeignKey(
        "tracking.Person",
        on_delete=models.CASCADE,
        related_name="person_status_changes",
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

    class Meta:
        verbose_name_plural = "Person Status Changes"

    def __str__(self):
        return f"{self.get_previous_display()} -> {self.get_next_display()}"


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


class RiskFactor(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Risk Factors"

    def __str__(self):
        return self.name


class Symptom(models.Model):
    name = models.CharField(max_length=255)
    rule = models.ForeignKey(
        "rules.LogicalCondition",
        related_name="symptoms",
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name


class PersonSymptomReport(TimeStampedModel):
    person = models.ForeignKey(
        "tracking.Person", on_delete=models.CASCADE, related_name="symptoms_reports"
    )
    symptom = models.ForeignKey(
        "tracking.Symptom", on_delete=models.CASCADE, related_name="persons"
    )

    def __str__(self):
        return f"{self.person}, {self.symptom}"
