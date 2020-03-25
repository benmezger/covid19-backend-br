from django.db import transaction

from tracking.models import Person
from .models import Notification, Rule


@transaction.atomic
def notification_create(
    *, person_beacon_id: str, rule_id: str, delivered: bool, read: bool
):
    person = Person.objects.get(beacon_id=person_beacon_id)
    rule = Rule.objects.get(id=rule_id)

    return Notification.objects.create(
        person=person, rule=rule, read=read, delivered=delivered,
    )
