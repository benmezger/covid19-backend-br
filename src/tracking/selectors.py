from typing import Iterable, List

from tracking.models import Person


def get_possible_infected_persons_in_ids(
    *, persons_beacons_ids: List[str]
) -> Iterable[Person]:
    return Person.objects.filter(beacon_id__in=persons_beacons_ids).filter(
        status__in=(Person.CONFIRMED, Person.SUSPECT)
    )
