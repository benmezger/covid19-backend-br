from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from tracking.models import Person, RiskFactor, Symptom


class PersonInputSerializer(serializers.Serializer):
    age = serializers.IntegerField()
    beacon_id = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=Person.objects.all())]
    )
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


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = ("id", "name")


class PersonSymptomnsReportInputSerializer(serializers.Serializer):
    symptoms_ids = serializers.ListField(child=serializers.IntegerField())
