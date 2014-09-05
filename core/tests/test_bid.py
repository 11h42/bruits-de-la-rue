from django.test import TestCase

from core.tests import factories


class BidTestCase(TestCase):
    def test_bid_to_json_method(self):
        user = factories.UserFactory()
        self.client.login(username=user.username, password="password")
        bid = factories.BidFactory(creator=user)
        expected_bid = {'begin': None, 'quantity': None, 'end': None, 'id': bid.id, 'title': 'Annonce de test',
                        'creator': user.username, 'description': bid.description, 'category': None, 'type': 'SUPPLY', 'real_author': 'Jean Dupont', 'localization': None}
        self.assertEquals(bid.serialize(), expected_bid)