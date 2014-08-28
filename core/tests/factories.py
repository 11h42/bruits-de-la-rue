# coding=utf-8
import factory
from factory.django import DjangoModelFactory


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = 'core.Address'
        django_get_or_create = ('recipient_name', 'address1', 'zipcode', 'town')

    recipient_name = 'Akema'
    address1 = '3 chemin de marticot'
    zipcode = '33610'
    town = 'Cestas'


class UserFactory(DjangoModelFactory):
    class Meta:
        model = 'core.User'
        django_get_or_create = ('username', 'email')

    username = 'test'
    email = 'test@akema.fr'
    password = factory.PostGenerationMethodCall('set_password',
                                                'password')


class BidFactory(DjangoModelFactory):
    class Meta:
        model = 'core.Bid'
        django_get_or_create = ('creator', 'description', 'title')

    creator = factory.SubFactory(UserFactory)
    description = "Factory d'une annonce"
    title = "Annonce de test"