# -*- coding: utf-8 -*-
import json
import datetime
from datetime import timedelta

from django.test import TestCase

from api.tests import factories
from api.tests.factories import BidFactory
from core import models
from core.models import Bid, bid_json_valid


class TestAuthentificationApi(TestCase):
    def test_get_bids_non_logged(self):
        response = self.client.get('/api/bids/')
        self.assertNotEquals(401, response.status_code)

    def test_post_a_bid_non_logged_return_302(self):
        response = self.client.post('/api/bids/', {})
        self.assertEquals(401, response.status_code)


class TestBidApi(TestCase):
    def setUp(self):
        self.begin = datetime.date.today()
        self.end = self.begin + timedelta(days=2)
        self.emergency_level = factories.EmergencyLevelFactory(name="Urgent", level=10)
        self.user = factories.UserFactory.create(email="toto@titi.com", password="1234")
        self.client.login(username=self.user.email, password="1234")
        self.bid = BidFactory(quantity_type='KG', name='test name', caller=self.user, begin=self.begin,
                              end=self.end, quantity="20", emergency_level=self.emergency_level, status='Ouvert')

    def test_get_a_bid(self):
        response = self.client.get('/api/bids/' + str(self.bid.id) + '/')
        self.assertEquals(200, response.status_code)
        bid = json.loads(response.content)
        expected_bid = json.dumps(self.bid.serialize())
        self.assertEquals(expected_bid, bid)

    def test_post_bid_create_bid_and_return_201(self):
        response = self.client.post('/api/bids/')
        self.assertEquals(201, response.status_code)
        bid = models.Bid.all()[0]
        self.assertEquals(bid, self.bid)


class TestBidsApi(TestCase):
    def setUp(self):
        self.begin = datetime.date.today()
        self.end = self.begin + timedelta(days=2)
        self.emergency_level = factories.EmergencyLevelFactory(name="Urgent", level=10)
        self.user = factories.UserFactory.create(email="toto@titi.com", password="1234")
        self.client.login(username=self.user.email, password="1234")
        self.bid = BidFactory(quantity_type='KG', name='test name', caller=self.user, begin=self.begin,
                              end=self.end, quantity="20", emergency_level=self.emergency_level, status='Ouvert')

    def test_get_bids_logged(self):
        response = self.client.get('/api/bids/')
        self.assertEquals(200, response.status_code)
        bids = json.loads(response.content)['bids']
        self.assertEquals(bids[0]['id'], self.bid.id)
        self.assertEquals(bids[0]['name'], 'test name')
        self.assertEquals(bids[0]['begin'], self.begin.isoformat())
        self.assertEquals(bids[0]['end'], self.end.isoformat())
        self.assertEquals(bids[0]['quantity'], 20)
        self.assertEquals(bids[0]['quantity_type'], 'KG')
        self.assertEquals(bids[0]['emergency_level'], self.emergency_level.id)
        self.assertEquals(bids[0]['time_left'], str(self.bid.end - self.bid.begin))
        self.assertEquals(bids[0]['status'], 'Ouvert')
        self.assertEquals(len(bids), 1)



    #
    # def test_create_a_bid_logged_with_miniaml_informations(self):
    #     login = self.client.login(username=self.user.email, password='1234')
    #     self.assertTrue(login)
    #     bid_category = factories.BidCategoryFactory(bid_category_name="Service")
    #     emergency = factories.EmergencyLevelFactory(name="FAIBLE", level=1)
    #     data = json.dumps({
    #         "caller": self.user.id,
    #         "name": "Fruits et légumes",
    #         "acceptor": "",
    #         "begin": str(datetime.datetime.today()),
    #         "end": str(datetime.datetime.today() + timedelta(days=2)),
    #         "quantity": str(12),
    #         "adress1": "Rue de la petite avenue",
    #         "adress2": "",
    #         "zipcode": "33000",
    #         "town": "Bordeaux",
    #         "country": "France",
    #         "real_author": "abriand",
    #         "description": "Ceci est une description",
    #         "bidCategory": bid_category.bid_category_name,
    #         "photo": "/images/default.png",
    #         "quantity_type": "KG",
    #         "status": "Ouvert",
    #         "type": "Offre",
    #         "emergency_level_level": emergency.level
    #     })
    #     response = self.client.post('/api/bids/', data, content_type='application/json')
    #
    #     bid_created = Bid.objects.filter(name="Fruits et légumes")[:1]
    #     self.assertTrue(bool(bid_created))