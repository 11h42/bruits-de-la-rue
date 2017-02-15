import factory
from factory.django import DjangoModelFactory

from core import models
from core.models import StatusBids


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = models.Address

    title = 'Akema'
    recipient_name = 'Akema'
    address1 = '3 chemin de marticot'
    zipcode = '33610'
    town = 'Cestas'


class UserFactory(DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Sequence(lambda n: 'user {0}'.format(n))
    email = 'test@akema.fr'
    password = factory.PostGenerationMethodCall('set_password', 'password')
    address = factory.RelatedFactory(AddressFactory)
    is_public_member = False


class AdminFactory(DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Sequence(lambda n: 'admin {0}'.format(n))
    email = 'admin@akema.fr'
    password = factory.PostGenerationMethodCall('set_password', 'password')
    address = factory.RelatedFactory(AddressFactory)
    is_public_member = False
    is_staff = True


class BidFactory(DjangoModelFactory):
    class Meta:
        model = models.Bid

    creator = factory.SubFactory(UserFactory)
    description = "factory d'une annonce"
    title = "Annonce de test"
    status_bid = StatusBids.RUNNING
    real_author = "Jean Dupont"


class AssociationFactory(DjangoModelFactory):
    class Meta:
        model = models.Association

    name = "Association Lambda"
    phone = '0123456789'
    url_site = 'example.org'
    email = 'contact@example.org'
    administrator = factory.SubFactory(UserFactory)


class BidCategoryFactory(DjangoModelFactory):
    class Meta:
        model = models.BidCategory

    name = 'category 1'


class FaqFactory(DjangoModelFactory):
    class Meta:
        model = models.Faq

    question = 'Q?'
    answer = 'a'
