from typing import Iterable, List, Union

from django.db import transaction
from django.contrib.auth import get_user_model

from .models import Person, PersonStatusChange, PersonRiskFactor, RiskFactor


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
    *, age: int, beacon_id: str, risk_factors_ids: List[Union[int, None]] = None
):
    person = Person.objects.create(age=age, beacon_id=beacon_id)

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
def risk_factors_get() -> Iterable[RiskFactor]:
    return RiskFactor.objects.all()


@transaction.atomic
def symptoms_get() -> Iterable[Symptom]:
    return Symptom.objects.all()


