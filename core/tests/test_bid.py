from django.test import TestCase
from core.models import StatusBids

from core.tests import factories


class BidTestCase(TestCase):
    def test_bid_to_json_method(self):
        self.maxDiff = None
        user = factories.UserFactory()
        self.client.login(username=user.username, password="password")
        bid = factories.BidFactory(creator=user)
        expected_bid = {'begin': None, 'quantity': None, 'end': None, 'id': bid.id, 'title': 'Annonce de test',
                        'creator': user.username, 'description': bid.description, 'category': None, 'type': 'SUPPLY',
                        'real_author': 'Jean Dupont', 'localization': None, 'status_bid': {'name': StatusBids.RUNNING},
                        'association': bid.association.serialize()}
        self.assertEquals(bid.serialize(), expected_bid)

    def test_bid_belong_to_user(self):
        creator = factories.UserFactory()
        bid = factories.BidFactory(creator=creator)

        self.assertTrue(bid.belong_to_user(creator))

        hacker = factories.UserFactory(username='hacker')
        self.assertFalse(bid.belong_to_user(hacker))
