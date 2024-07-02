import factory
from user.models import User

from faker import Faker

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    email = factory.Sequence(lambda n: "person{}@example.com".format(n))
    password = factory.PostGenerationMethodCall("set_password", "passer@@@111")
    is_active = "True"
    firstname = fake.name()
    lastname = fake.name()
