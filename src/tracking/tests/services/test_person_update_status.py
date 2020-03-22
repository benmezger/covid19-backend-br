from tracking.models import Person
from tracking.services import person_update_status


def test_person_update_status(make_person, make_user):
    person = make_person(status="D")
    user = make_user()

    last_status = person.status

    person = person_update_status(person=person, health_professional=user, status="C",)

    person = Person.objects.get(beacon_id="146d50f3-a488-45bf-afb3-9e9b1baabd49")
    person_status_change = person.person_status_changes.last()

    assert person.status == "C"

    assert person_status_change.person == person
    assert person_status_change.next == "C"
    assert person_status_change.previous == "D"
    assert person_status_change.health_professional == user
