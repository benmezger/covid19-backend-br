from typing import Dict, List

from .models import (
    RiskFactor,
    Symptom,
)


def get_symptoms_list() -> List[Dict[int, str]]:
    return list(Symptom.objects.values())


def get_risk_factors_list() -> List[Dict[int, str]]:
    return list(RiskFactor.objects.values())
