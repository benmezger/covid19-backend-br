from tracking.models import PersonEncounters
from tracking.services import person_encounters_create


def test_person_encounters_create(make_person):
    person = make_person(beacon_id="l0l8x1cz371tipdoxqn4ainhqojbdcf5lort")
    encounters = [
        "do8lrt4n5iny85eyw7gwbi7bcf6rcir0gsb7",
        "77l91d6vnyohlhek4ynuj1rtsrftbdjiqdpa",
        "fghcga6rl6jgjj31dfu9u5znefz1eqe1ielh",
    ]

    _ = person_encounters_create(
        person_beacon_id=person.beacon_id, encountered_persons_beacons_ids=encounters,
    )

    person_encounters = PersonEncounters.objects.first()

    assert person_encounters

    assert person_encounters.person_beacon_id == person.beacon_id
    assert person_encounters.encountered_persons_beacons_ids == encounters
