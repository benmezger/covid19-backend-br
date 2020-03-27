from tracking.models import Symptom
from tracking.selectors import get_symptoms_list


def test_get_symptoms_list(list_of_symptoms):
    list_of_symptoms()
    returned_list = get_symptoms_list()
    assert returned_list == list(Symptom.objects.values())
