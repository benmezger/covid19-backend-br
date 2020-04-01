from collections import OrderedDict
from datetime import datetime, timedelta

from tracking.models import Encounter
from tracking.services import encounter_bulk_create


def test_encounter_create(make_person, make_user):
    encounters_data = []

    person_one = make_person(beacon_id="123123123210")
    person_two = make_person(beacon_id="0129302909")

    for _ in range(2):
        start_date = datetime.now().timestamp()
        end_date = (datetime.now() + timedelta(hours=10)).timestamp()

        encounters_data.append(
            OrderedDict(
                person_two_beacon_id=person_two.beacon_id,
                start_date=start_date,
                end_date=end_date,
                duration=10,
                min_distance=10.0,
                count=1,
            )
        )

    encounter_bulk_create(
        person_one_beacon_id=person_one.beacon_id, encounters_data=encounters_data
    )

    assert Encounter.objects.count() == 2
