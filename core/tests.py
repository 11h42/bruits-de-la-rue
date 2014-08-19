from django.test import TestCase
from django.core.urlresolvers import reverse
from core import factories, views
from models import Bid


class BidTest(TestCase):
    def test_create_new_bid(self):
        self.user = factories.UserFactory()
        login = self.client.login(username=self.user.email, password="password")
        self.assertTrue(login)
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

        self.assertEquals('Tomates', Bid.objects.get(name="Tomates"))


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
