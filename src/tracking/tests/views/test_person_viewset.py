import json

from django.urls import reverse

from tracking.models import Person, PersonStatusChange, PersonSymptomReport


def test_person_create_empty_values(client, db, make_risk_factor):
    payload = {
        "beacon_id": "146d50f3-a488-45bf-afb3-9e9b1baabd49",
        "risk_factors_ids": [],
    }

    response = client.post(
        reverse("tracking:person-list"), data=payload, content_type="application/json"
    )

    assert response.status_code == 201

    person = Person.objects.get(beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")

    data = response.json()

    assert data["token"]
    assert (
        data.items()
        >= {
            "id": person.id,
            "age": None,
            "sex": None,
            "beacon_id": "146d50f3-a488-45bf-afb3-9e9b1baabd49",
            "status": "D",
        }.items()
    )

    assert person.risk_factors.count() == 0


def test_person_create(client, db, make_risk_factor):
    risk_factor_1 = make_risk_factor(name="Doença cardíaca")
    risk_factor_2 = make_risk_factor(name="Diabetes")

    payload = {
        "age": 50,
        "sex": "M",
        "beacon_id": "146d50f3-a488-45bf-afb3-9e9b1baabd49",
        "risk_factors_ids": [risk_factor_1.id, risk_factor_2.id],
    }

    response = client.post(
        reverse("tracking:person-list"), data=payload, content_type="application/json"
    )

    assert response.status_code == 201

    person = Person.objects.get(beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")

    data = response.json()

    assert data["token"]
    assert (
        data.items()
        >= {
            "id": person.id,
            "age": 50,
            "sex": "M",
            "beacon_id": "146d50f3-a488-45bf-afb3-9e9b1baabd49",
            "status": "D",
        }.items()
    )

    assert person.risk_factors.count() == 2


def test_person_create_existing_beacon_id(client, db, make_person, make_risk_factor):
    person = make_person(beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")

    risk_factor_1 = make_risk_factor(name="Doença cardíaca")
    risk_factor_2 = make_risk_factor(name="Diabetes")

    payload = {
        "age": 50,
        "sex": "U",
        "beacon_id": "146d50f3-a488-45bf-afb3-9e9b1baabd49",
        "risk_factors_ids": [risk_factor_1.id, risk_factor_2.id],
    }

    response = client.post(
        reverse("tracking:person-list"), data=payload, content_type="application/json"
    )

    person = Person.objects.get(beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")

    assert response.status_code == 400
    assert response.json() == {"beacon_id": ["This field must be unique."]}

    assert person.risk_factors.count() == 0


def test_person_create_without_risk_factors(client, db):
    payload = {
        "age": 50,
        "sex": "M",
        "beacon_id": "146d50f3-a488-45bf-afb3-9e9b1baabd49",
        "risk_factors_ids": [],
    }

    response = client.post(
        reverse("tracking:person-list"), data=payload, content_type="application/json"
    )

    assert response.status_code == 201

    person = Person.objects.get(beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")

    data = response.json()

    assert data["token"]
    assert (
        data.items()
        >= {
            "id": person.id,
            "age": 50,
            "sex": "M",
            "beacon_id": "146d50f3-a488-45bf-afb3-9e9b1baabd49",
            "status": "D",
        }.items()
    )

    assert person.risk_factors.count() == 0


def test_person_update_unauthenticated(client, db, make_person):
    person = make_person()

    payload = {"status": "C"}

    response = client.post(
        reverse(
            "tracking:person-update-status", kwargs={"beacon_id": person.beacon_id}
        ),
        data=payload,
        content_type="application/json",
    )

    assert response.status_code == 401


def test_person_update_authenticated_person(client, db, make_person):
    person = make_person()

    payload = {"status": "C"}

    response = client.post(
        reverse(
            "tracking:person-update-status", kwargs={"beacon_id": person.beacon_id}
        ),
        data=payload,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {person.token}",
    )

    assert response.status_code == 401


def test_person_update(client, db, make_person, make_user):
    user = make_user()
    person = make_person(beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")

    payload = {"status": "C"}

    response = client.post(
        reverse(
            "tracking:person-update-status", kwargs={"beacon_id": person.beacon_id}
        ),
        data=payload,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {user.token}",
    )

    person = Person.objects.get(beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")

    assert response.status_code == 200
    assert response.json() == {
        "id": person.id,
        "age": person.age,
        "sex": None,
        "beacon_id": person.beacon_id,
        "status": "C",
    }

    person_status_change = person.person_status_changes.last()

    assert person_status_change.person == person
    assert person_status_change.next == "C"
    assert person_status_change.previous == "D"
    assert person_status_change.health_professional == user


def test_person_update_unexisting_user(client, db, make_person, make_user):
    user = make_user()
    person = make_person(beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")

    payload = {"status": "C"}

    response = client.post(
        reverse("tracking:person-update-status", kwargs={"beacon_id": "wrong_id"}),
        data=payload,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Token {user.token}",
    )

    assert response.status_code == 404


def test_person_create_person_symptons(client, db, make_person, make_symptom):
    person = make_person(beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")
    symptom_1 = make_symptom("Diarreia")
    symptom_2 = make_symptom("Dor de cabeça")

    payload = {"symptoms_ids": [symptom_1.id, symptom_2.id]}

    response = client.post(
        reverse("tracking:person-symptoms-report"),
        data=payload,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"PersonToken {person.token}",
    )

    assert response.status_code == 201
    assert PersonSymptomReport.objects.count() == 2


def test_person_get_notifications(client, db, make_person, make_notification):
    person = make_person(beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")
    notification_one = make_notification(person=person)
    notification_two = make_notification(person=person)

    response = client.get(
        reverse("tracking:person-notification"),
        content_type="application/json",
        HTTP_AUTHORIZATION=f"PersonToken {person.token}",
    )

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_person_get(client, db, make_person):
    person = make_person(
        beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49", age=70, sex="M", status="R"
    )

    response = client.get(
        reverse("tracking:person-status"),
        content_type="application/json",
        HTTP_AUTHORIZATION=f"PersonToken {person.token}",
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "R",
    }
