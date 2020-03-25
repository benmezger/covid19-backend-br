import json

from django.urls import reverse

from notification.models import Notification


def test_notification_create(client, db, make_person, make_rule):
    person = make_person()
    rule = make_rule()

    payload = {
        "person_beacon_id": person.beacon_id,
        "rule_id": rule.pk,
        "delivered": True,
        "read": False,
    }

    response = client.post(
        reverse("notification:notification-list"),
        data=payload,
        content_type="application/json",
    )

    assert Notification.objects.count() == 1
    notification = Notification.objects.last()

    assert response.status_code == 201


def test_notification_update(client, db, make_notification):
    notification = make_notification()

    payload = {"read": True}

    response = client.patch(
        reverse("notification:notification-detail", kwargs={"pk": notification.pk}),
        data=payload,
        content_type="application/json",
    )

    notification = Notification.objects.get(pk=notification.pk)
    assert notification.read == True

    assert response.status_code == 200
