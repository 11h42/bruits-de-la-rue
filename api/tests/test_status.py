import json

from django.test.testcases import TestCase

from core.tests import factories


class TestStatus(TestCase):
    def setUp(self):
        user = factories.UserFactory()
        self.client.login(username=user.username, password="password")

    def test_get_status(self):
        return_bid_status = []

        resonse = self.client.get('/api/bids/status/')
        self.assertEquals(200, resonse.status_code)
        self.assertEquals({'status':[u'FERME', u'ACCEPTE', u'EN COURS', u'EN ATTENTE']}, json.loads(resonse.content))