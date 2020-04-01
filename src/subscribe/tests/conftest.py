import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from subscribe.tests.factories import SubscribeFactory

register(SubscribeFactory)


@pytest.fixture
def drf_client():
    return APIClient()
