from tracking.models import Person
from tracking.selectors import get_possible_infected_persons_in_ids


def test_get_possible_infected_persons_in_ids(db, make_person):
    person_1 = make_person(beacon_id="111111111111", status=Person.UNKNOWN)
    person_2 = make_person(beacon_id="222222222222", status=Person.SUSPECT)
    person_3 = make_person(beacon_id="333333333333", status=Person.RECOVERED)
    person_4 = make_person(beacon_id="444444444444", status=Person.CONFIRMED)
    person_5 = make_person(beacon_id="555555555555", status=Person.NEGATIVATED)
    person_6 = make_person(beacon_id="666666666666", status=Person.CONFIRMED)
    person_7 = make_person(beacon_id="777777777777", status=Person.CONFIRMED)

    interactions_ids = [
        "111111111111",
        "222222222222",
        "444444444444",
        "555555555555",
        "777777777777",
    ]

    queryset = get_possible_infected_persons_in_ids(
        persons_beacons_ids=interactions_ids
    )

    assert list(queryset.values_list("beacon_id", flat=True)) == [
        "222222222222",
        "444444444444",
        "777777777777",
    ]
