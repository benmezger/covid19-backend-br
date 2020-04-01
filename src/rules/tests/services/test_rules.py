import pytest
from django.core.exceptions import ValidationError

from rules import services
from rules.models import LogicalCondition, Rule, RuleCondition


@pytest.mark.django_db
def test_rule_create(rule_condition_factory):
    rule_cond = rule_condition_factory.create()
    rule = services.rule_create(
        name="Rule name", message="A rule message", rule_condition=rule_cond,
    )

    assert isinstance(rule, Rule)
    assert rule.name == "Rule name"
    assert rule.message == "A rule message"
    assert rule_cond in rule.conditions.all()


@pytest.mark.django_db
def test_rule_create_without_rule_condition(rule_condition_factory):
    rule_cond = rule_condition_factory.create()
    rule = services.rule_create(name="Rule name", message="A rule message",)

    assert isinstance(rule, Rule)
    assert rule.name == "Rule name"
    assert rule.message == "A rule message"
    assert rule_cond not in rule.conditions.all()


@pytest.mark.django_db
def test_rule_condition_create(rule_factory, logical_condition_factory):
    rule = rule_factory.create()
    logical = logical_condition_factory.create()
    cond = services.rule_condition_create(rule=rule, condition=logical)

    assert isinstance(cond, RuleCondition)
    assert cond.logical_conditions.all().first() == logical
    assert cond.rule == rule


@pytest.mark.django_db
def test_logical_condition_create(rule_factory):
    rule = rule_factory.create()
    logical = services.logical_condition_create(
        attribute="age",
        operator="gte",
        value="40",
        rule_condition=rule.conditions.first(),
    )

    assert isinstance(logical, LogicalCondition)
    assert logical.operator == "gte"
    assert logical.attribute == "age"
    assert logical.value == "40"
    assert logical.rule_condition == rule.conditions.first()


@pytest.mark.django_db
def test_logical_condition_create_with_invalid_attribute():
    with pytest.raises(ValidationError) as excinfo:
        services.logical_condition_create(
            attribute="foobar", operator="gte", value="40"
        )

    assert "Invalid attribute or operator" in excinfo.value


@pytest.mark.django_db
def test_logical_condition_create_with_invalid_operator():
    with pytest.raises(ValidationError) as excinfo:
        services.logical_condition_create(
            attribute="age", operator="foobar", value="40"
        )

    assert "Invalid attribute or operator" in excinfo.value


@pytest.mark.django_db
def test_logical_condition_lookup_query(logical_condition_factory):
    logical = logical_condition_factory.create(
        attribute="age", operator="gte", value="12"
    )

    assert logical.lookup_query == {f"age__gte": "12"}


@pytest.mark.django_db
def test_get_rule_condition_lookups(rule_factory, logical_condition_factory):
    rule = rule_factory.create()
    logical_condition_factory.create_batch(5, rule_condition=rule.conditions.first())
    lookups = services.get_rule_condition_lookups(rule.conditions.first())
    required_lookups = {}

    for cond in rule.conditions.first().logical_conditions.all():
        required_lookups.update(cond.lookup_query)

    assert required_lookups == lookups
