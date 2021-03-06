from datetime import datetime

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from faker import Faker

from notification.models import Notification
from rules.models import Rule
from tracking.models import (
    Encounter,
    Person,
    PersonEncounters,
    PersonStatusChange,
    RiskFactor,
    Symptom,
)

fake = Faker()

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
        user.is_staff = True
        user.set_password(raw_password=password)
        user.save()

        return user

    yield _make_user


@pytest.fixture
def make_person(db):
    def _make_person(
        age=70, beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49", status="D", sex=None
    ):
        return Person.objects.create(
            age=age, beacon_id=beacon_id, status=status, sex=sex
        )

    yield _make_person


@pytest.fixture
def make_person_status_change(db):
    def _make_person_status_change(make_person, make_user):
        person = make_person()
        health_professional = make_user()

        return PersonStatusChange.objects.create(
            person=person,
            previous=Person.UNKNOWN,
            next=Person.RECOVERED,
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


@pytest.fixture
def list_of_symptoms(db):
    def _list_of_symptoms(size=10):
        symptoms = []
        for i in range(size):
            symptoms.append(Symptom.objects.create(name=fake.name()))
        return symptoms

    yield _list_of_symptoms


@pytest.fixture
def make_encounter(db):
    def _make_encounter(
        person_one, person_two, start_date, end_date, min_distance, duration, count,
    ):
        return Encounter.objects.create(
            person_one=person_one,
            person_two=person_two,
            start_date=start_date,
            end_date=end_date,
            min_distance=min_distance,
            duration=duration,
            count=count,
        )

    yield _make_encounter


@pytest.fixture
def make_person_encounters(db):
    def _make_person_encounters(
        person_beacon_id, encountered_people_beacons_ids,
    ):
        return PersonEncounters.objects.create(
            person_beacon_id=person_beacon_id,
            encountered_people_beacons_ids=encountered_people_beacons_ids,
        )

    yield _make_person_encounters


@pytest.fixture
def make_notification(db, make_person, make_rule):
    def _make_notification(person=None, rule=None, read=False):
        if not person:
            person = make_person()

        if not rule:
            rule = make_rule()

        return Notification.objects.create(person=person, rule=rule, read=read,)

    yield _make_notification


@pytest.fixture
def make_rule(db):
    def _make_rule(name="Título", message="Mensagem"):
        return Rule.objects.create(name=name, message=message)

    yield _make_rule


@pytest.fixture(scope="session")
def create_rules_from_json_dump(django_db_setup, django_db_blocker):
    def _create_rules_from_json_dump(path="src/rules/tests/fixtures/rule_objects.json"):
        with django_db_blocker.unblock():
            call_command("loaddata", path)

    yield _create_rules_from_json_dump
