from rest_framework import serializers

from rules.models import LogicalCondition


class LogicalConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogicalCondition
        fields = (
            "attribute",
            "operator",
            "value",
        )
