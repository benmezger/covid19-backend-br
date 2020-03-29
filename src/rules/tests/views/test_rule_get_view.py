from django.urls import reverse


def test_rule_get(db, client, create_rules_from_json_dump, make_person):
    person = make_person()
    create_rules_from_json_dump()

    response = client.get(
        reverse("rules-list"), HTTP_AUTHORIZATION=f"PersonToken {person.token}"
    )

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


def test_rule_get_empty(db, client, make_person):
    person = make_person()

    response = client.get(
        reverse("rules-list"), HTTP_AUTHORIZATION=f"PersonToken {person.token}"
    )

    assert response.status_code == 200
    assert response.json() == []


def test_rule_get_unauthenticated(db, client):
    response = client.get(reverse("rules-list"))

    assert response.status_code == 401
