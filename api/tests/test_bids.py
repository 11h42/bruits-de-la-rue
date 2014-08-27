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

    def test_get_a_bid_and_returns_200(self):
        """
        To get a particular bid you should make a get on /api/bid/{bid_id}.
        This test check if the json contains the good informations  and if the api url is good.
        """
        bid = BidFactory(creator=self.user)
        response = self.client.get('/api/bid/' + str(bid.id) + '/')
        bids = json.loads(response.content)['bids']

        self.assertEquals(len(bids), 1)
        self.assertEquals(bids[0]['id'], bid.id)
        self.assertEquals(bids[0]['title'], 'Annonce de test')

        self.assertEquals(200, response.status_code)


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