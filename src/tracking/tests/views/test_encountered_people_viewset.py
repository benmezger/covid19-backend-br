from datetime import datetime, timedelta

from constance.test import override_config as constance_override_config
from django.urls import reverse
from freezegun import freeze_time

from tracking.models import Person, PersonEncounters


@constance_override_config(INCUBATION_DAYS=14)
def test_encountered_people(client, db, make_person, make_person_encounters):
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
        encountered_people_beacons_ids=[
            person_two.beacon_id,
            person_three.beacon_id,
            person_four.beacon_id,
        ],
    )
    make_person_encounters(
        person_beacon_id=person_two.beacon_id,
        encountered_people_beacons_ids=[
            person_one.beacon_id,
            person_three.beacon_id,
            person_four.beacon_id,
            person_seven.beacon_id,
        ],
    )

    old_encounters = [
        person_eight.beacon_id,
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
        "people_beacons_ids": [
            person_two.beacon_id,
            person_five.beacon_id,
            person_six.beacon_id,
        ]
    }

    response = client.post(
        reverse("tracking:encountered-people"),
        data=payload,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"PersonToken {person_one.token}",
    )

    assert PersonEncounters.objects.count() == 3
    assert (
        PersonEncounters.objects.filter(person_beacon_id=person_one.beacon_id).count()
        == 2
    )

    assert response.status_code == 200
    assert response.json() == [
        {"beacon_id": person_two.beacon_id, "status": "C",},
        {"beacon_id": person_five.beacon_id, "status": "C",},
        {"beacon_id": person_six.beacon_id, "status": "S",},
    ]


@constance_override_config(INCUBATION_DAYS=14)
def test_unencountered_people(client, db, make_person, make_person_encounters):
    person_one = make_person(beacon_id="q6yuu5d3h6y9dxghjf99tqw9ci3ya8reab5i")
    person_two = make_person(
        beacon_id="5nk2nqnjfs26a183oqeflumfhhswzm616lo1", status="R"
    )
    person_three = make_person(
        beacon_id="do8lrt4n5iny85eyw7gwbi7bcf6rcir0gsb7", status="U"
    )
    person_four = make_person(
        beacon_id="77l91d6vnyohlhek4ynuj1rtsrftbdjiqdpa", status="R"
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
    person_eight = make_person(
        beacon_id="j6h4uhfvcitfpsqwom0lyb3jpy5re2z3sw1q", status="S"
    )
    person_nine = make_person(
        beacon_id="sozxr1zibcitra0a5be7amzjopndxmdfzcps", status="C"
    )

    make_person_encounters(
        person_beacon_id=person_one.beacon_id,
        encountered_people_beacons_ids=[
            person_two.beacon_id,
            person_three.beacon_id,
            person_four.beacon_id,
        ],
    )
    make_person_encounters(
        person_beacon_id=person_two.beacon_id,
        encountered_people_beacons_ids=[
            person_one.beacon_id,
            person_three.beacon_id,
            person_four.beacon_id,
            person_seven.beacon_id,
        ],
    )

    old_encounters = [
        person_eight.beacon_id,
        person_nine.beacon_id,
    ]

    with freeze_time(datetime.now() - timedelta(days=14)):
        make_person_encounters(person_one.beacon_id, old_encounters)

    payload = {
        "people_beacons_ids": [
            person_two.beacon_id,
            person_five.beacon_id,
            person_six.beacon_id,
        ]
    }

    assert PersonEncounters.objects.count() == 3

    assert (
        PersonEncounters.objects.filter(person_beacon_id=person_one.beacon_id).count()
        == 2
    )

    response = client.post(
        reverse("tracking:encountered-people"),
        data=payload,
        content_type="application/json",
        HTTP_AUTHORIZATION=f"PersonToken {person_one.token}",
    )

    assert PersonEncounters.objects.count() == 3
    assert (
        PersonEncounters.objects.filter(person_beacon_id=person_one.beacon_id).count()
        == 2
    )

    assert response.status_code == 200
    assert response.json() == []


def test_encountered_people_unauthenticated(client, db, make_person):
    person = make_person(beacon_id="a488-45bf-afb3-9e9b1baabd49146-d50f3", status="D")
    person = make_person(beacon_id="9e9b1baabd49-146d50f3-a488-45bf-afb3", status="D")
    person = make_person(beacon_id="22222222-a488-45bf-9e9b1bafb3-aabd49", status="D")
    person = make_person(beacon_id="33333333-a488-45bf-afb3-9e9b1baabd49", status="D")
    person = make_person(beacon_id="44444444-a488-45bf-afb3-9e9b1baabd49", status="D")
    person = make_person(beacon_id="55555555-a488-45bf-afb3-9e9b1baabd49", status="D")

    payload = {
        "people_beacons_ids": [
            "a488-45bf-afb3-9e9b1baabd49146-d50f3",
            "9e9b1baabd49-146d50f3-a488-45bf-afb3",
            "22222222-a488-45bf-9e9b1bafb3-aabd49",
            "33333333-a488-45bf-afb3-9e9b1baabd49",
            "44444444-a488-45bf-afb3-9e9b1baabd49",
            "55555555-a488-45bf-afb3-9e9b1baabd49",
        ]
    }

    response = client.post(
        reverse("tracking:encountered-people"),
        data=payload,
        content_type="application/json",
    )

    assert response.status_code == 401
