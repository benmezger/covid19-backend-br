from typing import Dict, Iterable, List

from tracking.models import Person, RiskFactor, Symptom


def get_possible_infected_persons_in_ids(
    *, persons_beacons_ids: List[str]
) -> Iterable[Person]:
    return Person.objects.filter(beacon_id__in=persons_beacons_ids).filter(
        status__in=(Person.CONFIRMED, Person.SUSPECT)
    )


def get_symptoms_list() -> List[Dict[int, str]]:
    return list(Symptom.objects.values())


def get_risk_factors_list() -> List[Dict[int, str]]:
    return list(RiskFactor.objects.values())
