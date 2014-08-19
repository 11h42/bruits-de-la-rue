from django.test import TestCase
from core import factories
from models import User


class TestFactories(TestCase):
    def test_UserFactory(self):
        user = factories.UserFactory()
        self.assertTrue(isinstance(user, User))
    def test_UserFactoryLogin(self):
        user = factories.UserFactory()
        login = self.client.login(username=user.email, password="password")
        self.assertTrue(login)