# -*- coding: utf-8 -*-
import json

from django.test import TestCase

from api.validators import BidValidator
from core.models import Bid
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
        self.validator = BidValidator()

    def test_get_a_bid_and_returns_200(self):
        """
        To get a particular bid you should make a get on /api/bid/{bid_id}.
        This test check if the json contains the good informations  and if the api url is good.
        """
        bid = BidFactory(creator=self.user)
        response = self.client.get('/api/bids/' + str(bid.id) + '/')
        bids = json.loads(response.content)['bids']

        self.assertEquals(len(bids), 1)
        self.assertEquals(bids[0]['id'], bid.id)
        self.assertEquals(bids[0]['title'], 'Annonce de test')

        self.assertEquals(200, response.status_code)

    def test_post_a_bid_with_minimum_info_and_return_201(self):
        """
        To create a new bid you should post on /api/bid/. This post should contains a JSON with the miniumum
        required fields.
        """

        response = self.client.post('/api/bids/',
                                    json.dumps({
                                        "title": "Ma première annonce wouhouhou test 1234",
                                        "description": 'Ceci est une description'
                                    }),
                                    content_type="application/json; charset=utf-8")
        bids = Bid.objects.all()
        self.assertEquals(len(bids), 1)
        self.assertEquals(u'Ma première annonce wouhouhou test 1234', bids[0].title)
        self.assertEquals(201, response.status_code)

    def test_post_a_bid_with_all_authorized_informations(self):
        response = self.client.post('/api/bids/',
                                    json.dumps({
                                        "title": "Ma première annonce wouhouhou test 1234",
                                        "description": 'Ceci est une description'
                                    }),
                                    content_type="application/json; charset=utf-8")
        bids = Bid.objects.all()
        self.assertEquals(len(bids), 1)
        self.assertEquals(u'Ma première annonce wouhouhou test 1234', bids[0].title)
        self.assertEquals(201, response.status_code)

    def test_bid_is_valid_with_bad_fields_returns_false(self):
        self.assertFalse(self.validator.bid_is_valid({}))
        self.assertFalse(self.validator.bid_is_valid({'description': ""}))
        self.assertFalse(self.validator.bid_is_valid({'title': "Toto", 'description': "Titi", "toto": "tata"}))

    def test_bid_is_valid_with_good_fields_returns_true(self):
        self.assertTrue(
            self.validator.bid_is_valid({'title': "Chaise", 'description': "Un siège, un dossier, 4 pieds"}))


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