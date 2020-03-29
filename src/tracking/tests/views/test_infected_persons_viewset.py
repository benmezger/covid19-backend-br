from django.urls import reverse

from constance.test import override_config as constance_override_config
from freezegun import freeze_time

from tracking.models import Person


@constance_override_config(INCUBATION_DAYS=14)
def test_infected_persons(client, db, make_person, make_person_encounters):
    person_one = make_person(beacon_id="q6yuu5d3h6y9dxghjf99tqw9ci3ya8reab5i")
    person_two = make_person(
        beacon_id="5nk2nqnjfs26a183oqeflumfhhswzm616lo1", status="C"
    )
    person_three = make_person(
        beacon_id="do8lrt4n5iny85eyw7gwbi7bcf6rcir0gsb7", status="R"
    )
    person_four = make_person(
        beacon_id="77l91d6vnyohlhek4ynuj1rtsrftbdjiqdpa", status="U"
    )
    person_five = make_person(
        beacon_id="fghcga6rl6jgjj31dfu9u5znefz1eqe1ielh", status="C"
    )
    person_six = make_person(
        beacon_id="v1omyn61wetd89gm000vxgjxhteoeyfd8s2q", status="S"
    )
    person_seven = make_person(
        beacon_id="0m97qdc3jf3f9w49lte9d1tio68q1fj74995", status="R"
    )
    person_eight = make_person(
        beacon_id="j6h4uhfvcitfpsqwom0lyb3jpy5re2z3sw1q", status="S"
    )
    person_nine = make_person(
        beacon_id="sozxr1zibcitra0a5be7amzjopndxmdfzcps", status="C"
    )

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

    old_encounters = [
        person_eigth.beacon_id,
        person_nine.beacon_id,
    ]

    with freeze_time(datetime.now() - timedelta(days=14)):
        make_person_encounters(person_one.beacon_id, old_encounters)

    assert PersonEncounters.objects.count() == 3

    assert (
        PersonEncounters.objects.filter(person_beacon_id=person_one.beacon_id).count()
        == 2
    )

    payload = {
        "persons_beacons_ids": [
            person_two.beacon_id,
            person_five.beacon_id,
            person_six.beacon_id,
        ]
    }

    # TODO: User authentication
    response = client.post(
        reverse("tracking:infected-persons"),
        data=payload,
        content_type="application/json",
    )

    assert PersonEncounters.objects.count() == 3
    assert (
        PersonEncounters.objects.filter(person_beacon_id=person_one.beacon_id).count()
        == 2
    )

    assert response.status_code == 200
    assert response.json() == [
        {"beacon_id": person_two.beacon_id, "status": "C",},
        {"beacon_id": person_five.beacon_id, "status": "S",},
        {"beacon_id": person_six.beacon_id, "status": "C",},
    ]


@constance_override_config(INCUBATION_DAYS=14)
def test_uninfected_persons(client, db, make_person, make_person_encounters):
    person_one = make_person(beacon_id="q6yuu5d3h6y9dxghjf99tqw9ci3ya8reab5i")
    person_two = make_person(
        beacon_id="5nk2nqnjfs26a183oqeflumfhhswzm616lo1", status="R"
    )
    person_three = make_person(
        beacon_id="do8lrt4n5iny85eyw7gwbi7bcf6rcir0gsb7", status="C"
    )
    person_four = make_person(
        beacon_id="77l91d6vnyohlhek4ynuj1rtsrftbdjiqdpa", status="U"
    )
    person_five = make_person(
        beacon_id="fghcga6rl6jgjj31dfu9u5znefz1eqe1ielh", status="R"
    )
    person_six = make_person(
        beacon_id="v1omyn61wetd89gm000vxgjxhteoeyfd8s2q", status="R"
    )
    person_seven = make_person(
        beacon_id="0m97qdc3jf3f9w49lte9d1tio68q1fj74995", status="R"
    )

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

    with freeze_time(datetime.now() - timedelta(days=14)):
        make_person_encounters(person_one.beacon_id, old_encounters)

    assert PersonEncounters.objects.count() == 3

    assert (
        PersonEncounters.objects.filter(person_beacon_id=person_one.beacon_id).count()
        == 2
    )

    payload = {
        "persons_beacons_ids": [
            person_two.beacon_id,
            person_five.beacon_id,
            person_six.beacon_id,
        ]
    }

    response = client.post(
        reverse("tracking:infected-persons"),
        data=payload,
        content_type="application/json",
    )

    assert PersonEncounters.objects.count() == 3
    assert (
        PersonEncounters.objects.filter(person_beacon_id=person_one.beacon_id).count()
        == 2
    )

    assert response.status_code == 200
    assert response.json() == []
