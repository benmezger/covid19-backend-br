import factory

from subscribe.models import Subscribe


class SubscribeFactory(factory.DjangoModelFactory):
    email = factory.Faker("email")

    class Meta:
        model = Subscribe
