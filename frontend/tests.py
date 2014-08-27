# Create your tests here.
from django.test import TestCase
from api.tests import factories
from frontend.views import return_email_if_username


class UserTest(TestCase):
    def test_function_return_email_if_username_with_non_existing_username(self):
        self.assertEquals(return_email_if_username("abriand1456"), None)

    def test_function_return_email_if_username_with_existing_username(self):
        self.user = factories.UserFactory(username="abriand", email="abriand@akema.fr")
        self.assertEquals(return_email_if_username("abriand"), self.user.email)

    def test_function_return_email_if_username_with_good_email(self):
        self.assertEquals(return_email_if_username("abriand@akema.fr"), "abriand@akema.fr")

    def test_function_return_email_if_username_with_bad_email(self):
        self.assertEquals(return_email_if_username("abri@and@akema.fr"), None)