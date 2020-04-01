import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_request_subscribe_form(drf_client, subscribe_factory):
    subscribe = subscribe_factory.build()
    request = drf_client.post(
        reverse("subscribe-list"), data={"email": subscribe.email}
    )

    assert request.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_request_with_invalid_subscribe_form(drf_client,):
    request = drf_client.post(reverse("subscribe-list"), data={"email": ""})

    assert request.status_code == status.HTTP_400_BAD_REQUEST
