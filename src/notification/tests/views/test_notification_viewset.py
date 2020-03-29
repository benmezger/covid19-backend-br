import json

from django.urls import reverse

from notification.models import Notification


def test_notification_create(client, db, make_person, make_rule):
    person = make_person()
    rule = make_rule()

    payload = {
        "rule_id": rule.pk,
        "delivered": True,
        "read": False,
    }

    response = client.post(
        reverse("notification:notification-list"),
        data=payload,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"PersonToken {person.token}",
    )

    assert Notification.objects.filter(person=person).count() == 1
    assert response.status_code == 201

    data = response.json()

    assert data["created"]
    assert data["id"]

    assert (
        data.items()
        >= {
            "title": rule.name,
            "message": rule.message,
            "delivered": True,
            "read": False,
        }.items()
    )


def test_notification_create_unauthenticated(client, db, make_person, make_rule):
    person = make_person()
    rule = make_rule()

    payload = {
        "rule_id": rule.pk,
        "delivered": True,
        "read": False,
    }

    response = client.post(
        reverse("notification:notification-list"),
        data=payload,
        content_type="application/json",
    )

    assert Notification.objects.filter(person=person).count() == 0
    assert response.status_code == 401


def test_notification_update(client, db, make_notification):
    notification = make_notification()

    payload = {"read": True}

    response = client.patch(
        reverse("notification:notification-detail", kwargs={"pk": notification.pk}),
        data=payload,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"PersonToken {notification.person.token}",
    )

    notification = Notification.objects.get(pk=notification.pk)
    assert notification.read == True

    assert response.status_code == 200


def test_notification_update_unauthenticated(client, db, make_notification):
    notification = make_notification()

    payload = {"read": True}

    response = client.patch(
        reverse("notification:notification-detail", kwargs={"pk": notification.pk}),
        data=payload,
        content_type="application/json",
    )

    notification = Notification.objects.get(pk=notification.pk)
    assert notification.read == False

    assert response.status_code == 401
