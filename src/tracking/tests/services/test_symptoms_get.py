from tracking.services import symptoms_get


def test_symptoms_get(make_symptom):
    symptom_1 = make_symptom(name="Dor de cabeça")
    symptom_2 = make_symptom(name="Diarreia")

    symptoms = symptoms_get()

    assert symptoms.filter(id__in=[symptom_1.id, symptom_2.id]).exists()
