import factory

from subscribe.models import Subscribe


class SubscribeFactory(factory.DjangoModelFactory):
    name = factory.Faker("name")
    email = factory.Faker("email")

    class Meta:
        model = Subscribe
