from tracking.services import risk_factors_get


def test_risk_factors_get(make_risk_factor):
    risk_factor_1 = make_risk_factor(name="Doença cardíaca")
    risk_factor_2 = make_risk_factor(name="Diabetes")

    risk_factors = risk_factors_get()

    assert risk_factors.filter(id__in=[risk_factor_1.id, risk_factor_2.id]).exists()
