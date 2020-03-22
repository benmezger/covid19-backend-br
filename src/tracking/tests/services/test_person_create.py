from tracking.models import Person
from tracking.services import person_create


def test_person_create(db):
    person = person_create(age=50, beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")

    person = Person.objects.get(beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")

    assert person.age == 50
    assert person.status == "D"
    assert person.beacon_id == "146d50f3-a488-45bf-afb3-9e9b1baabd49"

    assert person.risk_factors.count() == 0


def test_person_create_with_risk_factors(db, make_risk_factor):
    risk_factor_1 = make_risk_factor(name="Doença cardíaca")
    risk_factor_2 = make_risk_factor(name="Diabetes")

    person = person_create(
        age=50,
        beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49",
        risk_factors_ids=[risk_factor_1.id, risk_factor_2.id],
    )

    person = Person.objects.get(beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")

    assert person.age == 50
    assert person.status == "D"
    assert person.beacon_id == "146d50f3-a488-45bf-afb3-9e9b1baabd49"

    assert person.risk_factors.count() == 2
