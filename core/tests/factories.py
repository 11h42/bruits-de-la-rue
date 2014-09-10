# coding=utf-8
import factory
from factory.django import DjangoModelFactory
from core.models import StatusBids


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = 'core.Address'
        django_get_or_create = ('recipient_name', 'address1', 'zipcode', 'town')

    title = 'Akema'
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

    @factory.post_generation
    def address(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for item in extracted:
                self.address.add(item)

    @factory.post_generation
    def associations(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for item in extracted:
                self.associations.add(item)


class AssociationFactory(DjangoModelFactory):
    class Meta:
        model = 'core.Association'
        django_get_or_create = ('name', 'phone', 'fax', 'url_site', 'email')

    name = "Association Lambda"
    phone = '0123456789'
    fax = '0987654321'
    url_site = 'association-lambda.com'
    email = 'contact@association-lambda.com'

    @factory.post_generation
    def address(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for item in extracted:
                self.address.add(item)


class BidFactory(DjangoModelFactory):
    class Meta:
        model = 'core.Bid'
        django_get_or_create = ('creator', 'description', 'title', 'status_bid', 'type', 'real_author')

    creator = factory.SubFactory(UserFactory)
    description = "Factory d'une annonce"
    title = "Annonce de test"
    type = "SUPPLY"
    status_bid = StatusBids.RUNNING
    real_author = "Jean Dupont"
    association = factory.SubFactory(AssociationFactory)


class BidCategoryFactory(DjangoModelFactory):
    class Meta:
        model = 'core.BidCategory'
        django_get_or_create = ('name', )

    name = "Alimentaire"


class FaqFactory(DjangoModelFactory):
    class Meta:
        model ='core.Faq'
        django_get_or_create = ('question', 'answer')

    question = 'Factored question'
    answer = 'Factored answer'