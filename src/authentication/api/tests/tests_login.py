import json

import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token

test_params = {
    "blank_values": (
        ("", ""),
        {
            "email": ["This field may not be blank."],
            "password": ["This field may not be blank."],
        },
    ),
    "blank_email": (
        ("", "password_value"),
        {"email": ["This field may not be blank."]},
    ),
    "blank_password": (
        ("email_value", ""),
        {"password": ["This field may not be blank."]},
    ),
}


@pytest.mark.parametrize(
    "payload, expected", test_params.values(), ids=list(test_params.keys())
)
def test_invalid_payload(client, payload, expected):
    payload = {"email": payload[0], "password": payload[1]}

    response = client.post(
        path=reverse("authentication:login"),
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json() == expected


def test_wrong_credentials(client, make_user):
    user = make_user(
        email="drauzio@gmail.com",
        first_name="Drauzio",
        last_name="Varella",
        password="password",
    )

    response = client.post(
        path=reverse("authentication:login"),
        data=json.dumps({"email": "drauzio@gmail.com", "password": "21stcentury"}),
        content_type="application/json",
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Email ou senha incorretos."}


def test_successful_login(client, make_user):
    user = make_user(
        email="drauzio@gmail.com",
        first_name="Drauzio",
        last_name="Varella",
        password="password",
    )
    response = client.post(
        path=reverse("authentication:login"),
        data=json.dumps({"email": "drauzio@gmail.com", "password": "password"}),
        content_type="application/json",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user"] == {
        "first_name": "Drauzio",
        "last_name": "Varella",
        "email": "drauzio@gmail.com",
    }
    assert len(data["access_token"]) > 10

    assert Token.objects.filter(user=user).exists()
