import json

from django.urls import reverse


def test_risk_factor_list(client, db, make_risk_factor):
    risk_factor_1 = make_risk_factor(name="Doença cardíaca")
    risk_factor_2 = make_risk_factor(name="Diabetes")

    response = client.get(reverse("risk-factor-list"), content_type="application/json")

    assert response.status_code == 200
    assert response.json() == [
        {"id": risk_factor_1.id, "name": risk_factor_1.name,},
        {"id": risk_factor_2.id, "name": risk_factor_2.name,},
    ]
