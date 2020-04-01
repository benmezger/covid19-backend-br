from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Dict, Iterable, List, Union

from constance import config
from django.contrib.auth import get_user_model
from django.db import transaction

from .models import (
    Encounter,
    Person,
    PersonEncounters,
    PersonRiskFactor,
    PersonStatusChange,
    PersonSymptomReport,
    RiskFactor,
    Symptom,
)

User = get_user_model()


@transaction.atomic
def person_risk_factor_bulk_create(
    *, person: Person, risk_factors: Iterable[RiskFactor]
) -> PersonRiskFactor:
    return PersonRiskFactor.objects.bulk_create(
        PersonRiskFactor(person=person, risk_factor=risk_factor)
        for risk_factor in risk_factors
    )


@transaction.atomic
def person_create(
    *,
    age: int = None,
    sex: str = None,
    beacon_id: str,
    risk_factors_ids: List[Union[int, None]] = None,
):
    person = Person.objects.create(age=age, beacon_id=beacon_id, sex=sex)

    if risk_factors_ids:
        risk_factors = RiskFactor.objects.filter(id__in=risk_factors_ids)
        person_risk_factor_bulk_create(person=person, risk_factors=risk_factors)

    return person


@transaction.atomic
def person_update_status(
    *, person: Person, health_professional: User, status: str
) -> Person:
    person_last_status = str(person.status)

    person_status_change_create(
        person=person,
        health_professional=health_professional,
        previous_status=person_last_status,
        next_status=status,
    )

    # caching purposes
    person.status = status
    person.save()

    return person


@transaction.atomic
def person_status_change_create(
    *, person: Person, health_professional: User, previous_status: str, next_status: str
) -> PersonStatusChange:
    return PersonStatusChange.objects.create(
        person=person,
        previous=previous_status,
        next=next_status,
        health_professional=health_professional,
    )


@transaction.atomic
def person_symptom_report_bulk_create(
    *, person: Person, symptoms_ids: List[int]
) -> Iterable[PersonSymptomReport]:
    symptoms = Symptom.objects.filter(id__in=symptoms_ids)

    return PersonSymptomReport.objects.bulk_create(
        PersonSymptomReport(person=person, symptom=symptom) for symptom in symptoms
    )


@transaction.atomic
def encounter_bulk_create(
    person_one_beacon_id: str, encounters_data: List[OrderedDict]
) -> None:
    Encounter.objects.bulk_create(
        encounter_create(person_one_beacon_id=person_one_beacon_id, **encounter_data)
        for encounter_data in encounters_data
    )


@transaction.atomic
def encounter_create(
    *,
    person_one_beacon_id: str,
    person_two_beacon_id: str,
    start_date: float,
    end_date: float,
    min_distance: float,
    duration: int,
    count: int,
    city: str = None,
) -> Encounter:

    person_one = Person.objects.get(beacon_id=person_one_beacon_id)
    person_two = Person.objects.get(beacon_id=person_two_beacon_id)

    return Encounter(
        person_one=person_one,
        person_two=person_two,
        start_date=datetime.fromtimestamp(start_date),
        end_date=datetime.fromtimestamp(end_date),
        min_distance=min_distance,
        duration=duration,
        city=city,
        count=count,
    )


@transaction.atomic
def person_encounters_create(
    *, person_beacon_id: str, encountered_people_beacons_ids: List[str],
) -> PersonEncounters:
    person_encounters_delete_older_encounters(person_beacon_id=person_beacon_id)

    return PersonEncounters.objects.create(
        person_beacon_id=person_beacon_id,
        encountered_people_beacons_ids=encountered_people_beacons_ids,
    )


@transaction.atomic
def person_encounters_delete_older_encounters(*, person_beacon_id: str) -> None:
    PersonEncounters.objects.filter(
        person_beacon_id=person_beacon_id,
        date__lt=datetime.now() - timedelta(days=config.INCUBATION_DAYS),
    ).delete()
