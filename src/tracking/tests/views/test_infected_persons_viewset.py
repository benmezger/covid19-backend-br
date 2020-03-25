import json

from django.urls import reverse

from tracking.models import Person, PersonStatusChange, PersonSymptomReport


def test_infected_persons(client, db, make_risk_factor):
    person = make_person(beacon_id="a488-45bf-afb3-9e9b1baabd49146-d50f3", status="D")
    person = make_person(beacon_id="9e9b1baabd49-146d50f3-a488-45bf-afb3", status="C")
    person = make_person(beacon_id="22222222-a488-45bf-9e9b1bafb3-aabd49", status="S")
    person = make_person(beacon_id="33333333-a488-45bf-afb3-9e9b1baabd49", status="C")
    person = make_person(beacon_id="44444444-a488-45bf-afb3-9e9b1baabd49", status="R")
    person = make_person(beacon_id="55555555-a488-45bf-afb3-9e9b1baabd49", status="D")

    payload = {
        [
            "a488-45bf-afb3-9e9b1baabd49146-d50f3",
            "9e9b1baabd49-146d50f3-a488-45bf-afb3",
            "22222222-a488-45bf-9e9b1bafb3-aabd49",
            "33333333-a488-45bf-afb3-9e9b1baabd49",
            "44444444-a488-45bf-afb3-9e9b1baabd49",
            "55555555-a488-45bf-afb3-9e9b1baabd49",
        ]
    }

    response = client.post(
        reverse("tracking:infected-persons"),
        data=payload,
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json() == {
        "persons": {
            "beacon_id": "blabla",
            "status": "blabla",
            "status_change_date": "blabla",
        },
        "rules": [],
    }
