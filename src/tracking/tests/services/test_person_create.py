from tracking.models import Person
from tracking.services import person_create


def test_person_create(db):
    person = person_create(age=50, beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")

    person = Person.objects.get(beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")

    assert person.age == 50
    assert person.status == "D"
    assert person.beacon_id == "146d50f3-a488-45bf-afb3-9e9b1baabd49"
