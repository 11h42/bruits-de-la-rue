from django.core.urlresolvers import reverse

from django.test import TestCase

from api.tests.factories import UserFactory, BidFactory


class TestBids(TestCase):

    def test_get_an_existing_bid(self):
        bid = BidFactory(name="MyBid")
        response = self.client.get(reverse('api:get-bid', kwargs={'pk': bid.id}))
        self.assertEquals(200, response.status_code)

