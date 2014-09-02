from django.test import TestCase

from core.models import User, BidCategories
from core.tests import factories
from core.tests.factories import AddressFactory, BidFactory


class TestFactories(TestCase):
    def test_address_factory(self):
        address = AddressFactory()
        self.assertEquals(address.recipient_name, 'Akema')

    def test_user_factory(self):
        user = factories.UserFactory()
        self.assertTrue(isinstance(user, User))
        self.assertEquals(user.email, 'test@akema.fr')

    def test_user_factory_is_authenticated(self):
        user = factories.UserFactory()
        is_authenticated = self.client.login(username=user.username, password="password")
        self.assertTrue(is_authenticated)

    def test_create_super_user(self):
        user = factories.UserFactory(username='superman', is_staff=True)
        self.assertTrue(isinstance(user, User))
        self.assertEquals(user.email, 'test@akema.fr')
        self.assertTrue(user.is_staff)

    def test_bid_factory(self):
        creator = factories.UserFactory(username='creator')
        bid = BidFactory(creator=creator)
        self.assertEquals(bid.title, 'Annonce de test')
        self.assertEquals(bid.creator, creator)
        self.assertEquals(bid.description, "Factory d'une annonce")

    def test_bid_category_factory(self):
        category = factories.BidCategoryFactory()

        self.assertEquals(category.name, BidCategories.objects.get(name=category.name).name)
