import factory
from term import models

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Faker('first_name')
    email = factory.LazyAttribute(lambda a: '{}@example.com'.format(a.username).lower())

class CategoryFactory(factory.django.DjangoModelFactory):
    title = 'Программалоо'
    class Meta:
        model = models.Category

class TermFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Term

    term = 'процессор'
    description = factory.Faker('sentence')
    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
