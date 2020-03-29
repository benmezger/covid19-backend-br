from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from tracking.models import Person, RiskFactor, Symptom


class EncounterInputSerializer(serializers.Serializer):
    person_two_beacon_id = serializers.CharField()
    start_date = serializers.FloatField()
    end_date = serializers.FloatField()
    min_distance = serializers.FloatField()
    duration = serializers.IntegerField()
    city = serializers.CharField(default=None)
    count = serializers.IntegerField(required=True)


class PersonInputSerializer(serializers.Serializer):
    age = serializers.IntegerField(required=False)
    sex = serializers.CharField(required=False)
    beacon_id = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=Person.objects.all())]
    )
    status = serializers.CharField(required=False)
    risk_factors_ids = serializers.ListField(child=serializers.IntegerField())


class PersonOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("id", "age", "sex", "beacon_id", "status")


class PersonStatusSerializer(serializers.Serializer):
    status = serializers.CharField()


class PersonCreationOutputSerializer(PersonOutputSerializer):
    class Meta(PersonOutputSerializer.Meta):
        fields = PersonOutputSerializer.Meta.fields + ("token",)


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


class EncounteredPeopleInputSerializer(serializers.Serializer):
    people_beacons_ids = serializers.ListField(child=serializers.CharField())


class EncounteredPeopleOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("beacon_id", "status")
