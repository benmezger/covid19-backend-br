from tracking.models import Symptom
from tracking.services import symptom_list


def test_symptoms_list(list_of_symptoms):
    list_of_symptoms()
    returned_list = symptom_list()
    assert returned_list == list(Symptom.objects.values())
