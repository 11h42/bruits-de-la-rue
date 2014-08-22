import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from api.tests.factories import BidFactory


class TestBids(TestCase):
    def test_get_an_existing_bid(self):
        bid = BidFactory()
        response = self.client.get(reverse('api:get-bid', kwargs={'bid_id': bid.id}))
        self.assertEquals(200, response.status_code)
        bid_json = json.loads(response.content)
        self.assertEquals(bid.name, bid_json.get('name'))

    def test_get_non_existing_bid(self):
        response = self.client.get(reverse('api:get-bid', kwargs={'bid_id': 4}))
        self.assertEquals(400, response.status_code)

