from django.db import transaction
from django.contrib.auth import get_user_model

from .models import Person, PersonStatusChange


User = get_user_model()


@transaction.atomic
def person_create(*, age: int, beacon_id: str):
    return Person.objects.create(age=age, beacon_id=beacon_id)


@transaction.atomic
def person_update_status(
    person: Person, health_professional: User, status: str
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
    person: Person, health_professional: User, previous_status: str, next_status: str
) -> PersonStatusChange:
    return PersonStatusChange.objects.create(
        person=person,
        previous=previous_status,
        next=next_status,
        health_professional=health_professional,
    )
