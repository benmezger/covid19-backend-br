import json

from django.urls import reverse


def test_symptom_list(client, db, make_symptom):
    symptom_1 = make_symptom(name="Dor de cabeça")
    symptom_2 = make_symptom(name="Dor de garganta")

    response = client.get(
        reverse("tracking:symptom-list"), content_type="application/json"
    )

    assert response.status_code == 200
    assert response.json() == [
        {"id": symptom_1.id, "name": symptom_1.name,},
        {"id": symptom_2.id, "name": symptom_2.name,},
    ]
