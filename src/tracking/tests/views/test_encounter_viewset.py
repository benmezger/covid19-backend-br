import json
from datetime import datetime, timedelta

from django.urls import reverse

from tracking.models import Encounter


def test_encounter_create(client, db, make_person):
    person_one = make_person(beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")
    person_two = make_person(beacon_id="a488-45bf-afb3-9e9b1baabd49-146d50f3")
    person_three = make_person(beacon_id="45bf-afb3-9e9b1baabd49-146d50f3-a488")

    payload = [
        {
            "person_two_beacon_id": "a488-45bf-afb3-9e9b1baabd49-146d50f3",
            "start_date": 1584905619.222456,
            "end_date": 1584905632.263027,
            "duration": 20,
            "min_distance": 40.0,
            "count": 1,
        },
        {
            "person_two_beacon_id": "45bf-afb3-9e9b1baabd49-146d50f3-a488",
            "start_date": 1584905619.222456,
            "end_date": 1584905632.263027,
            "duration": 10,
            "min_distance": 10.0,
            "count": 1,
        },
    ]

    response = client.post(
        reverse("tracking:encounter-list"),
        data=payload,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"PersonToken {person_one.token}",
    )

    assert Encounter.objects.count() == 2
    assert Encounter.objects.filter(person_one=person_one).count() == 2

    assert response.status_code == 201


def test_encounter_create_unauthenticated(client, db, make_person):
    person_one = make_person(beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")
    person_two = make_person(beacon_id="a488-45bf-afb3-9e9b1baabd49-146d50f3")
    person_three = make_person(beacon_id="45bf-afb3-9e9b1baabd49-146d50f3-a488")

    payload = [
        {
            "person_two_beacon_id": "a488-45bf-afb3-9e9b1baabd49-146d50f3",
            "start_date": 1584905619.222456,
            "end_date": 1584905632.263027,
            "duration": 20,
            "min_distance": 40.0,
            "count": 1,
        },
        {
            "person_two_beacon_id": "45bf-afb3-9e9b1baabd49-146d50f3-a488",
            "start_date": 1584905619.222456,
            "end_date": 1584905632.263027,
            "duration": 10,
            "min_distance": 10.0,
            "count": 1,
        },
    ]

    response = client.post(
        reverse("tracking:encounter-list"),
        data=payload,
        content_type="application/json",
    )

    assert Encounter.objects.count() == 0
    assert Encounter.objects.filter(person_one=person_one).count() == 0

    assert response.status_code == 401


def test_encounter_create_count(client, db, make_person, make_encounter):
    person_one = make_person(beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")
    person_two = make_person(beacon_id="45bf-afb3-9e9b1baabd49-146d50f3-a488")

    start_date = datetime.now()
    end_date = datetime.now() + timedelta(hours=10)

    for _ in range(5):
        make_encounter(
            person_one=person_one,
            person_two=person_two,
            start_date=start_date,
            end_date=end_date,
            duration=10,
            min_distance=10.0,
            count=1,
        )

    make_encounter(
        person_one=person_two,
        person_two=person_one,
        start_date=start_date,
        end_date=end_date,
        duration=10,
        min_distance=10.0,
        count=1,
    )

    response = client.get(
        reverse("tracking:encounter-count"),
        content_type="application/json",
        HTTP_AUTHORIZATION=f"PersonToken {person_one.token}",
    )

    assert response.status_code == 200
    assert response.json() == {"count": 5}
