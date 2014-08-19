from django.test import TestCase
from django.core.urlresolvers import reverse
from core import factories
from models import Bid


class OffersTests(TestCase):
    def test_create_new_offer(self):
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