from typing import Dict, Iterable, List, Set

from tracking.models import Person, PersonEncounters, RiskFactor, Symptom


def get_person_encounters_unique_encountered_people_beacons_ids(
    *, person_beacon_id: str
) -> Set[str]:
    flat_encountered_people = PersonEncounters.objects.filter(
        person_beacon_id=person_beacon_id
    ).values_list("encountered_people_beacons_ids", flat=True)

    return set(flatten(flat_encountered_people))


def get_people_encountered_with_disease_statuses(
    *, person_beacon_id: str
) -> Iterable[Person]:
    encountered_people_beacons_ids = get_person_encounters_unique_encountered_people_beacons_ids(
        person_beacon_id=person_beacon_id
    )

    return Person.objects.filter(beacon_id__in=encountered_people_beacons_ids).filter(
        status__in=(Person.CONFIRMED, Person.SUSPECT)
    )


def get_symptoms_list() -> List[Dict[int, str]]:
    return list(Symptom.objects.values())


def get_risk_factors_list() -> List[Dict[int, str]]:
    return list(RiskFactor.objects.values())


def flatten(nested_list):
    for each_list in nested_list:
        for item in each_list:
            yield item
