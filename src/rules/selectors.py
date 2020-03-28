from rules.models import RuleCondition


def rule_condition_has_logical(
    rule_condition: RuleCondition, attribute: str, **kwargs
) -> bool:
    return bool(
        rule_condition.logical_conditions.filter(attribute=attribute, **kwargs).count()
    )
