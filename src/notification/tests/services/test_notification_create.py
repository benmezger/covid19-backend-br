from notification.models import Notification
from notification.services import notification_create


def test_notification_create(db, make_rule, make_person):
    person = make_person(age=50, beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")
    rule = make_rule()

    notification = notification_create(
        person_beacon_id=person.beacon_id, rule_id=rule.pk, delivered=True, read=False
    )

    assert notification.read == False
    assert notification.delivered == True
    assert notification.person == person
    assert notification.rule == rule
