# -*- coding: utf-8 -*-
import json

from django.test import TestCase

from core.tests.factories import BidFactory
from core.tests import factories


class TestAuthApi(TestCase):
    def test_get_bids_non_logged(self):
        response = self.client.get('/api/bids/')
        self.assertEquals(401, response.status_code)

    def test_post_a_bid_non_logged_return_401(self):
        response = self.client.post('/api/bids/', {})
        self.assertEquals(401, response.status_code)


class TestBidApi(TestCase):
    def setUp(self):
        self.user = factories.UserFactory()
        self.client.login(username=self.user.username, password="password")
    #
    # def test_GET_bid_200(self):
    #     bid = BidFactory(creator=self.user)
    #     response = self.client.get('/api/bids/' + str(bid.id) + '/')
    #     self.assertEquals(200, response.status_code)
    #     bid = json.loads(response.content)
    #     expected_bid = json.dumps(bid.serialize())
    #     self.assertEquals(expected_bid, bid)


class TestBidsApi(TestCase):
    def setUp(self):
        self.user = factories.UserFactory()
        self.client.login(username=self.user.username, password="password")

    def test_get_bids_empty(self):
        response = self.client.get('/api/bids/')
        self.assertEquals(200, response.status_code)
        bids = json.loads(response.content)['bids']
        self.assertEquals(bids, [])

    def test_get_bids_200(self):
        bid = BidFactory(creator=self.user)
        response = self.client.get('/api/bids/')
        self.assertEquals(200, response.status_code)
        bids = json.loads(response.content)['bids']
        self.assertEquals(len(bids), 1)
        self.assertEquals(bids[0]['id'], bid.id)
        self.assertEquals(bids[0]['title'], 'Annonce de test')
