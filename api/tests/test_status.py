import json

from django.test.testcases import TestCase
from core.models import StatusBids

from core.tests import factories


class TestStatus(TestCase):
    def setUp(self):
        user = factories.UserFactory()
        self.client.login(username=user.username, password="password")

    def test_get_status(self):
        return_bid_status = []
        for e in StatusBids.TYPE_CHOICES:
            return_bid_status.append({str(e[0]): str(e[0])})
        resonse = self.client.get('/api/bids/status/')
        self.assertEquals(200, resonse.status_code)
        self.assertEquals(return_bid_status, json.loads(resonse.content))