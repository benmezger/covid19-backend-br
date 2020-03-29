from datetime import datetime, timedelta

from constance.test import override_config as constance_override_config
from freezegun import freeze_time

from tracking.models import PersonEncounters
from tracking.services import person_encounters_delete_older_encounters


@constance_override_config(INCUBATION_DAYS=14)
def test_person_encounters_delete_older_than(make_person, make_person_encounters):
    person_one = make_person(beacon_id="q6yuu5d3h6y9dxghjf99tqw9ci3ya8reab5i")
    person_two = make_person(beacon_id="5nk2nqnjfs26a183oqeflumfhhswzm616lo1")

    encounters = [
        "do8lrt4n5iny85eyw7gwbi7bcf6rcir0gsb7",
        "77l91d6vnyohlhek4ynuj1rtsrftbdjiqdpa",
        "fghcga6rl6jgjj31dfu9u5znefz1eqe1ielh",
    ]

    make_person_encounters(person_one.beacon_id, encounters)
    make_person_encounters(person_two.beacon_id, encounters)

    old_encounters = [
        "v1omyn61wetd89gm000vxgjxhteoeyfd8s2q",
        "0m97qdc3jf3f9w49lte9d1tio68q1fj74995",
        "do8lrt4n5iny85eyw7gwbi7bcf6rcir0gsb7",
    ]

    with freeze_time(datetime.now() - timedelta(days=14)):
        make_person_encounters(person_one.beacon_id, old_encounters)

    assert PersonEncounters.objects.count() == 3
    assert (
        PersonEncounters.objects.filter(person_beacon_id=person_one.beacon_id).count()
        == 2
    )

    person_encounters_delete_older_encounters(person_beacon_id=person_one.beacon_id,)

    assert PersonEncounters.objects.count() == 2
    assert (
        PersonEncounters.objects.filter(person_beacon_id=person_one.beacon_id).count()
        == 1
    )


@constance_override_config(INCUBATION_DAYS=14)
def test_person_encounters_delete_older_than_do_not_delete_rows(
    make_person, make_person_encounters
):
    person_one = make_person(beacon_id="q6yuu5d3h6y9dxghjf99tqw9ci3ya8reab5i")
    person_two = make_person(beacon_id="5nk2nqnjfs26a183oqeflumfhhswzm616lo1")

    encounters = [
        "do8lrt4n5iny85eyw7gwbi7bcf6rcir0gsb7",
        "77l91d6vnyohlhek4ynuj1rtsrftbdjiqdpa",
        "fghcga6rl6jgjj31dfu9u5znefz1eqe1ielh",
    ]

    make_person_encounters(person_one.beacon_id, encounters)
    make_person_encounters(person_two.beacon_id, encounters)

    old_encounters = [
        "v1omyn61wetd89gm000vxgjxhteoeyfd8s2q",
        "0m97qdc3jf3f9w49lte9d1tio68q1fj74995",
        "do8lrt4n5iny85eyw7gwbi7bcf6rcir0gsb7",
    ]

    with freeze_time(datetime.now() - timedelta(days=13)):
        make_person_encounters(person_one.beacon_id, old_encounters)

    assert PersonEncounters.objects.count() == 3
    assert (
        PersonEncounters.objects.filter(person_beacon_id=person_one.beacon_id).count()
        == 2
    )

    person_encounters_delete_older_encounters(person_beacon_id=person_one.beacon_id,)

    assert PersonEncounters.objects.count() == 3
    assert (
        PersonEncounters.objects.filter(person_beacon_id=person_one.beacon_id).count()
        == 2
    )
