from django.db import models
from django_extensions.db.models import TimeStampedModel

from rules.datatypes import ConditionAttribute, ConditionOperator


class Rule(TimeStampedModel):
    name = models.CharField(
        max_length=255, null=False, blank=False, verbose_name="Name"
    )

    message = models.CharField(
        max_length=255, null=False, blank=False, verbose_name="Message"
    )
    enabled = models.BooleanField(null=False, default=True, blank=False)
    any = models.BooleanField(default=True, null=False)

    def __str__(self):
        return f"{self.name}"


class RuleCondition(TimeStampedModel):
    rule = models.ForeignKey(
        "rules.Rule",
        null=True,
        blank=True,
        verbose_name="Rule",
        on_delete=models.SET_NULL,
        related_name="conditions",
    )

    def __str__(self):
        return f"Rule Condition: {self.rule}"


class LogicalCondition(TimeStampedModel):
    rule_condition = models.ForeignKey(
        "rules.RuleCondition",
        verbose_name="Condition",
        on_delete=models.CASCADE,
        related_name="logical_conditions",
    )

    attribute = models.CharField(
        max_length=20,
        choices=ConditionAttribute.choices(),
        null=False,
        blank=False,
        verbose_name="Attribute",
    )

    operator = models.CharField(
        max_length=10,
        choices=ConditionOperator.choices(),
        null=False,
        blank=False,
        verbose_name="Operator",
    )

    value = models.CharField(
        max_length=100, null=False, blank=False, verbose_name="Value",
    )

    def __str__(self):
        return f"Logical Condition: {self.rule_condition.rule}"

    @property
    def lookup_query(self):
        return {f"{self.attribute}__{self.operator}": self.value}
