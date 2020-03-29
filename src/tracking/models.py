from django.db import models
from django.utils.translation import gettext as _
from django_extensions.db.models import TimeStampedModel

from .managers import EncounterManager


class Person(models.Model):
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

    MALE = "M"
    FEMALE = "F"
    NOT_DECLARED = "N"

    SEX_STATUS_CHOICES = (
        (MALE, _("Masculino")),
        (FEMALE, _("Feminino")),
        (NOT_DECLARED, _("Não declarar")),
    )

    age = models.PositiveIntegerField(null=True)
    sex = models.CharField(choices=SEX_STATUS_CHOICES, null=True, max_length=1)
    status = models.CharField(
        choices=PERSON_STATUS_CHOICES, default=UNKNOWN, max_length=1
    )
    beacon_id = models.CharField(unique=True, max_length=36)

    def __str__(self):
        return f"Status: {self.get_status_display()}"


class PersonStatusChange(TimeStampedModel):
    person = models.ForeignKey(
        "tracking.Person",
        on_delete=models.CASCADE,
        related_name="person_status_changes",
    )
    previous = models.CharField(
        choices=Person.PERSON_STATUS_CHOICES, default=Person.UNKNOWN, max_length=1
    )
    next = models.CharField(
        choices=Person.PERSON_STATUS_CHOICES, default=Person.UNKNOWN, max_length=1
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
    rule = models.ForeignKey(
        "rules.LogicalCondition",
        related_name="risk_factors",
        null=True,
        on_delete=models.SET_NULL,
    )

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


class Encounter(models.Model):
    person_one = models.ForeignKey(
        "tracking.Person",
        on_delete=models.SET_NULL,
        related_name="encounters_as_first_person",
        null=True,
        blank=True,
    )
    person_two = models.ForeignKey(
        "tracking.Person",
        on_delete=models.SET_NULL,
        related_name="encounters_as_second_person",
        null=True,
        blank=True,
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration = models.PositiveIntegerField()
    min_distance = models.FloatField()

    count = models.PositiveIntegerField(null=False, default=0)
    city = models.CharField(null=True, blank=True, max_length=250)

    objects = EncounterManager()

    def __str__(self):
        return f"{self.person_one} - {self.person_two}"
