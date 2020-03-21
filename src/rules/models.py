from django.db import models
from django_extensions.db.models import TimeStampedModel

from rules.datatypes import ConditionAttribute, ConditionOperator


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


class RuleCondition(TimeStampedModel):
    rule = models.ForeignKey(
        "rules.Rule",
        null=True,
        verbose_name="Regra",
        on_delete=models.SET_NULL,
        related_name="conditions",
    )


class LogicalCondition(TimeStampedModel):
    rule_condition = models.ForeignKey(
        "rules.RuleCondition",
        verbose_name="Condicao",
        on_delete=models.CASCADE,
        related_name="logical_conditions",
    )

    attribute = models.CharField(
        max_length=10,
        choices=ConditionAttribute.choices(),
        null=False,
        blank=False,
        verbose_name="Atributo",
    )

    operator = models.CharField(
        max_length=10,
        choices=ConditionOperator.choices(),
        null=False,
        blank=False,
        verbose_name="Operador",
    )

    value = models.CharField(
        max_length=100, null=False, blank=False, verbose_name="Valor",
    )
