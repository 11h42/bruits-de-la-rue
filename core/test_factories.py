from django.test import TestCase

from api.tests import factories
from models import User


class TestFactories(TestCase):
    def test_user_factory(self):
        user = factories.UserFactory()
        self.assertTrue(isinstance(user, User))

    def test_user_factory_login(self):
        user = factories.UserFactory()
        login = self.client.login(username=user.email, password="password")
        self.assertTrue(login)