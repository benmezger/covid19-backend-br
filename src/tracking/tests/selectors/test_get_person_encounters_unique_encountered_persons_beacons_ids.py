from tracking.models import PersonEncounters
from tracking.selectors import (
    get_person_encounters_unique_encountered_persons_beacons_ids,
)


def test_get_person_encounters_unique_encountered_persons_beacons_ids(
    make_person, make_person_encounters
):
    person_one = make_person(beacon_id="q6yuu5d3h6y9dxghjf99tqw9ci3ya8reab5i")
    person_two = make_person(beacon_id="5nk2nqnjfs26a183oqeflumfhhswzm616lo1")
    person_three = make_person(beacon_id="do8lrt4n5iny85eyw7gwbi7bcf6rcir0gsb7")
    person_four = make_person(beacon_id="77l91d6vnyohlhek4ynuj1rtsrftbdjiqdpa")
    person_five = make_person(beacon_id="fghcga6rl6jgjj31dfu9u5znefz1eqe1ielh")
    person_six = make_person(beacon_id="v1omyn61wetd89gm000vxgjxhteoeyfd8s2q")
    person_seven = make_person(beacon_id="0m97qdc3jf3f9w49lte9d1tio68q1fj74995")

    make_person_encounters(
        person_beacon_id=person_one.beacon_id,
        encountered_persons_beacons_ids=[
            person_two.beacon_id,
            person_three.beacon_id,
            person_four.beacon_id,
        ],
    )
    make_person_encounters(
        person_beacon_id=person_two.beacon_id,
        encountered_persons_beacons_ids=[
            person_one.beacon_id,
            person_three.beacon_id,
            person_four.beacon_id,
            person_seven.beacon_id,
        ],
    )
    make_person_encounters(
        person_beacon_id=person_one.beacon_id,
        encountered_persons_beacons_ids=[
            person_two.beacon_id,
            person_five.beacon_id,
            person_six.beacon_id,
        ],
    )

    expected = {
        person_two.beacon_id,
        person_three.beacon_id,
        person_four.beacon_id,
        person_five.beacon_id,
        person_six.beacon_id,
    }

    assert (
        get_person_encounters_unique_encountered_persons_beacons_ids(
            person_beacon_id=person_one.beacon_id,
        )
        == expected
    )
