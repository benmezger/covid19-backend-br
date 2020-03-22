import pytest
from django.contrib.auth import get_user_model

from tracking.models import (
    Person,
    PersonStatusChange,
    RiskFactor,
    Symptom,
    UNKNOWN,
    SUSPECT,
    RECOVERED,
    CONFIRMED,
    NEGATIVATED,
)

User = get_user_model()


@pytest.fixture
def make_user(db):
    def _make_user(
        email="drauzio@gmail.com",
        first_name="Drauzio",
        last_name="Varella",
        password="password",
    ):
        user = User.objects.create(
            email=email, first_name=first_name, last_name=last_name
        )
        user.set_password(raw_password=password)
        user.save()

        return user

    yield _make_user


@pytest.fixture
def make_person(db):
    def _make_person(
        age=70, beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49", status="D"
    ):
        return Person.objects.create(age=age, beacon_id=beacon_id, status=status)

    yield _make_person


@pytest.fixture
def make_person_status_change(db):
    def _make_person_status_change(make_person, make_user):
        person = make_person()
        health_professional = make_user()

        return PersonStatusChange.objects.create(
            person=person,
            previous=UNKNOWN,
            next=RECOVERED,
            health_professional=health_professional,
        )

    yield _make_person_status_change


@pytest.fixture
def make_risk_factor(db):
    def _make_risk_factor(name="Doença cardíaca"):
        return RiskFactor.objects.create(name=name)

    yield _make_risk_factor


@pytest.fixture
def make_symptom(db):
    def _make_symptom(name="Diarreia"):
        return Symptom.objects.create(name=name)

    yield _make_symptom
