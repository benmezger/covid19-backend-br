from django.core.exceptions import ValidationError

from rules.datatypes import ConditionAttribute, ConditionOperator
from rules.models import LogicalCondition, Rule, RuleCondition


def rule_create(name: str, message: str, rule_condition: RuleCondition = None) -> Rule:
    rule = Rule.objects.create(name=name, message=message)

    if rule_condition:
        rule.conditions.add(rule_condition)

    return rule


def rule_condition_create(rule: Rule, condition: LogicalCondition) -> RuleCondition:
    rule_condition, _ = RuleCondition.objects.get_or_create(rule=rule)
    rule_condition.logical_conditions.add(condition)
    return rule_condition


def logical_condition_create(
    attribute: str, operator: str, value: str, rule_condition: RuleCondition = None
) -> LogicalCondition:

    if not (
        ConditionAttribute.has_key(attribute) and ConditionOperator.has_value(operator)
    ):
        raise ValidationError("Invalid attribute or operator")

    logical, _ = LogicalCondition.objects.get_or_create(
        attribute=attribute,
        operator=operator,
        value=value,
        rule_condition=rule_condition,
    )
    return logical


def get_rule_condition_lookups(rule_condition: RuleCondition) -> dict:
    lookups = {}
    for cond in rule_condition.logical_conditions.all():
        lookups.update(cond.lookup_query)
    return lookups
