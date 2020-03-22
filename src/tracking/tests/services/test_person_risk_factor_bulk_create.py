from tracking.models import PersonRiskFactor
from tracking.services import person_risk_factor_bulk_create


def test_person_risk_factor_create(db, make_person, make_risk_factor):
    risk_factor_1 = make_risk_factor()
    risk_factor_2 = make_risk_factor()
    person = make_person()

    person_risk_factor = person_risk_factor_bulk_create(
        person=person, risk_factors=[risk_factor_1, risk_factor_2]
    )

    assert PersonRiskFactor.objects.filter(person=person).count() == 2
