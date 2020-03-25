from pytest_factoryboy import register
from rules.tests.factories import (
    RuleFactory,
    RuleConditionFactory,
    LogicalConditionFactory,
)

register(RuleFactory)
register(RuleConditionFactory)
register(LogicalConditionFactory)
