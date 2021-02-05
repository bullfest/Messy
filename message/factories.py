import factory


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.LazyAttribute(
        lambda u: f"{u.first_name.lower()}_{u.last_name.lower()}"
    )

    class Meta:
        model = "auth.User"
        django_get_or_create = ("username",)


class MessageFactory(factory.django.DjangoModelFactory):
    recipient = factory.SubFactory(UserFactory)
    content = factory.Faker("paragraph", nb_sentences=5)

    class Meta:
        model = "message.Message"


class MessageWithSenderFactory(MessageFactory):
    sender = factory.SubFactory(UserFactory)

    class Meta:
        model = "message.Message"
