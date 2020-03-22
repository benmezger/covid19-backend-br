from rest_framework import serializers

from tracking.models import Person, RiskFactor


class PersonInputSerializer(serializers.Serializer):
    age = serializers.IntegerField()
    beacon_id = serializers.CharField()
    status = serializers.CharField(required=False)
    risk_factors_ids = serializers.ListField(child=serializers.IntegerField())


class PersonOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("id", "age", "beacon_id", "status")


class RiskFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskFactor
        fields = ("id", "name")
