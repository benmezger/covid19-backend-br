from tracking.models import PersonSymptomReport
from tracking.services import person_symptom_report_bulk_create


def test_person_symptom_report_bulk_create(db, make_person, make_symptom):
    symptom_1 = make_symptom("Diarreia")
    symptom_2 = make_symptom("Dor de cabeça")
    person = make_person()

    person_symptom = person_symptom_report_bulk_create(
        person=person, symptoms_ids=[symptom_1.id, symptom_2.id]
    )

    assert PersonSymptomReport.objects.filter(person=person).count() == 2
