from datetime import datetime, timedelta

from tracking.services import encounter_create


def test_encounter_create(make_person, make_user):
    start_date = datetime.now().timestamp()
    end_date = (datetime.now() + timedelta(hours=10)).timestamp()

    person_one = make_person(beacon_id="123123123210")
    person_two = make_person(beacon_id="0129302909")

    encounter = encounter_create(
        person_one_beacon_id=person_one.beacon_id,
        person_two_beacon_id=person_two.beacon_id,
        start_date=start_date,
        end_date=end_date,
        duration=10,
        min_distance=10.0,
        count=1,
    )

    assert encounter.person_one == person_one
    assert encounter.person_two == person_two
    assert encounter.start_date == datetime.fromtimestamp(start_date)
    assert encounter.end_date == datetime.fromtimestamp(end_date)
    assert encounter.min_distance == 10.0
    assert encounter.duration == 10
    assert encounter.count == 1
