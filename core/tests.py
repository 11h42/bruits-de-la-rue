from django.test import TestCase

from api.tests import factories
from core import views


class BidTest(TestCase):
    def setUp(self):
        self.user = factories.UserFactory(email="abriand@akema.fr", password="1234")
        login = self.client.login(username=self.user.email, password="1234")
        self.assertTrue(login)


"""
    def test_create_new_bid(self):
        self.client.post(reverse('core:offer_add'),
                         {'name': 'Tomates',
                          'type': 'toto',
                          'begin': '2014/12/12',
                          'end': '2015/12/12',
                          'status': 'TheStatus',
                          'quantity': 12,
                          'localization': 'Toronto',
                          'real_author': 'Antoine',
                          'emergency_level': 'Faible',
                          'recurrence': False,
                          'description': "This is a description",
                          'bidCategory': "This is a bid category"})

        self.assertEquals('Tomates', Bid.objects.get(name="Tomates")) """


class UserTest(TestCase):
    def test_function_return_email_if_username_with_non_existing_username(self):
        self.assertEquals(views.return_email_if_username("abriand1456"), None)

    def test_function_return_email_if_username_with_existing_username(self):
        self.user = factories.UserFactory(username="abriand", email="abriand@akema.fr")
        self.assertEquals(views.return_email_if_username("abriand"), self.user.email)

    def test_function_return_email_if_username_with_good_email(self):
        self.assertEquals(views.return_email_if_username("abriand@akema.fr"), "abriand@akema.fr")

    def test_function_return_email_if_username_with_bad_email(self):
        self.assertEquals(views.return_email_if_username("abri@and@akema.fr"), None)
