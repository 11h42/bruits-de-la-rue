from django.test import TestCase

from api.tests import factories
from core.models import User


class TestFactories(TestCase):
    def test_user_factory(self):
        user = factories.UserFactory()
        self.assertTrue(isinstance(user, User))
        self.assertEquals(user.email, 'factory_user@akema.fr')

    def test_user_factory_is_authenticated(self):
        user = factories.UserFactory()
        is_authenticated = self.client.login(username=user.email, password="password")
        self.assertTrue(is_authenticated)