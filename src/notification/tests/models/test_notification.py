from notification.models import Notification


def test_notification(db, make_person, make_rule):
    person = make_person()
    rule = make_rule(name="Título", message="Mensagem")

    notification = Notification.objects.create(
        person=person, rule=rule, read=False, delivered=True
    )

    assert notification.title == "Título"
    assert notification.message == "Mensagem"
