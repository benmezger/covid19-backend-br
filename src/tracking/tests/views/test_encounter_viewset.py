import json

from django.urls import reverse

from tracking.models import Encounter


def test_encounter_create(client, db, make_person):
    person_one = make_person(beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")
    person_two = make_person(beacon_id="a488-45bf-afb3-9e9b1baabd49-146d50f3")

    payload = {
        "person_one_beacon_id": "146d50f3-a488-45bf-afb3-9e9b1baabd49",
        "person_two_beacon_id": "a488-45bf-afb3-9e9b1baabd49-146d50f3",
        "start_date": 1584905619.222456,
        "end_date": 1584905632.263027,
        "duration": 10,
        "min_distance": 10.0,
    }

    response = client.post(
        reverse("tracking:encounter-list"),
        data=payload,
        content_type="application/json",
    )

    assert Encounter.objects.count() == 1

    assert response.status_code == 201
