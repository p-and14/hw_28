import factory
import faker

from ads.models import Ad, Category
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    birth_date = "2000-01-01"
    email = factory.Faker("ascii_free_email")
    username = factory.Faker("name")
    password = "test_password"


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("name")
    slug = factory.Faker("first_name")


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = factory.Faker("name")
    author = factory.SubFactory(UserFactory)
    price = 100
    category = factory.SubFactory(CategoryFactory)
