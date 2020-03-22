import factory
from factory.fuzzy import FuzzyChoice

from rules.datatypes import ConditionAttribute, ConditionOperator
from rules.models import LogicalCondition, Rule, RuleCondition


class RuleFactory(factory.DjangoModelFactory):
    class Meta:
        model = Rule

    name = factory.Faker("catch_phrase")
    message = factory.Faker("paragraph")
    conditions = factory.RelatedFactory(
        "rules.tests.factories.RuleConditionFactory", "rule"
    )


class RuleConditionFactory(factory.DjangoModelFactory):
    class Meta:
        model = RuleCondition

    logical_conditions = factory.RelatedFactory(
        "rules.tests.factories.LogicalConditionFactory", "rule_condition",
    )


class LogicalConditionFactory(factory.DjangoModelFactory):
    class Meta:
        model = LogicalCondition

    attribute = FuzzyChoice((i[0] for i in ConditionAttribute.choices()))
    operator = FuzzyChoice((i[1] for i in ConditionOperator.choices()))
    value = FuzzyChoice((10, 20, 30, 40, 50, 60))

    rule_condition = factory.SubFactory("rules.tests.factories.RuleConditionFactory",)
