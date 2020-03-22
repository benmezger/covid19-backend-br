from tracking.services import person_status_change_create


def test_person_status_change_create(make_person, make_user):
    person = make_person()
    user = make_user()

    person_status_change = person_status_change_create(
        person=person, health_professional=user, previous_status="U", next_status="C"
    )

    assert person_status_change.person == person
    assert person_status_change.next == "C"
    assert person_status_change.previous == "U"
    assert person_status_change.health_professional == user
