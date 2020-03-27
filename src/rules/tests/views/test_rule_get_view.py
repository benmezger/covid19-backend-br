import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_rule_get(client, create_rules_from_json_dump):
    create_rules_from_json_dump()
    response = client.get(reverse("rules-list"))
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "Rule 1",
            "message": "Hello rule 1",
            "logical_conditions": [
                {"attribute": "encounter_distance", "operator": "lt", "value": "12"},
                {"attribute": "age", "operator": "gt", "value": "12"},
            ],
        },
        {
            "name": "Rule 2",
            "message": "Hello rule 2",
            "logical_conditions": [
                {"attribute": "age", "operator": "gt", "value": "12"}
            ],
        },
    ]


@pytest.mark.django_db
def test_rule_get_empty(client):
    response = client.get(reverse("rules-list"))
    assert response.status_code == 200
    assert response.json() == []
