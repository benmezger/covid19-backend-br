from rest_framework import serializers

from rules.models import LogicalCondition, RuleCondition


class LogicalConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogicalCondition
        fields = (
            "attribute",
            "operator",
            "value",
        )


class RuleConditionSerializer(serializers.ModelSerializer):
    logical_conditions = LogicalConditionSerializer(many=True, read_only=True)

    class Meta:
        model = RuleCondition
        fields = ("logical_conditions",)
