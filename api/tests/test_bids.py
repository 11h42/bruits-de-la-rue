# -*- coding: utf-8 -*-
import json
import datetime

from django.test import TestCase

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

    def test_get_a_bid_and_returns_200(self):
        """
        To get a particular bid you should make a get on /api/bid/{bid_id}.
        This test check if the json contains the good informations  and if the api url is good.
        """
        bid = BidFactory(creator=self.user)
        response = self.client.get('/api/bids/' + str(bid.id) + '/')
        returned_bid = json.loads(response.content)
        self.assertEquals(returned_bid['id'], bid.id)
        self.assertEquals(returned_bid['title'], 'Annonce de test')

        self.assertEquals(200, response.status_code)

    def test_post_a_bid_with_all_required_fields(self):
        response = self.client.post('/api/bids/',
                                    json.dumps({
                                        "title": "Ma première annonce wouhouhou test 1234",
                                        "description": 'Ceci est une description',
                                        "type": "OFFER",
                                    }),
                                    content_type="application/json; charset=utf-8")
        bids = Bid.objects.all()
        self.assertEquals(len(bids), 1)
        self.assertEquals(u'Ma première annonce wouhouhou test 1234', bids[0].title)
        self.assertEquals(201, response.status_code)

    def test_post_a_bid_with_all_authorized_fields(self):
        today = datetime.datetime.today()
        tomorrow = today + datetime.timedelta(days=1)
        category = factories.BidCategoryFactory()
        bid = {'title': 'My bid',
               'description': 'The bid description',
               'type': 'OFFER',
               'begin': today.isoformat(),
               'end': tomorrow.isoformat(),
               'category': category.name,
               'quantity': 2}
        response = self.client.post('/api/bids/', json.dumps(bid), content_type="application/json; charset=utf-8")
        bid = Bid.objects.get(title=bid['title'])
        self.assertEquals(201, response.status_code)
        self.assertEquals(u'My bid', bid.title)

    def test_accept_bid(self):
        creator = factories.UserFactory(username='bid creator')
        bid = factories.BidFactory(creator=creator)

        response = self.client.put('/api/bids/%s/' % bid.id, json.dumps({'status': 'ACCEPTED'}))
        self.assertEquals(200, response.status_code)

        bid_accepted = Bid.objects.get(id=bid.id)
        self.assertEquals("ACCEPTED", bid_accepted.status)
        self.assertEquals(self.user, bid_accepted.purchaser)

    def test_cant_accept_bid_that_belong_to_the_user(self):
        bid = factories.BidFactory(creator=self.user)

        response = self.client.put('/api/bids/%s/' % bid.id, json.dumps({'status': 'ACCEPTED'}))
        self.assertEquals(403, response.status_code)

        bid_non_modified = Bid.objects.get(id=bid.id)
        self.assertEquals("RUNNING", bid_non_modified.status)
        self.assertEquals(None, bid_non_modified.purchaser)

    def test_delete_bid_owned(self):
        bid = factories.BidFactory(creator=self.user)

        response = self.client.delete('/api/bids/%s/' % bid.id)
        self.assertEquals(204, response.status_code)

    def test_delete_bid_not_owned(self):
        bid = factories.BidFactory(creator=factories.UserFactory(username="OtherUser"))

        response = self.client.delete('/api/bids/%s/' % bid.id)
        self.assertEquals(403, response.status_code)

    def test_delete_bid_not_owned_with_superuser_account(self):
        self.client.logout()
        superuser = factories.UserFactory(username="Superman", is_staff=True)
        login = self.client.login(username=superuser.username, password='password')
        self.assertTrue(login)
        bid = factories.BidFactory(creator=self.user)

        response = self.client.delete('/api/bids/%s/' % bid.id)
        self.assertEquals(204, response.status_code)


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

    def test_post_a_bid_with_minimum_info_and_return_201(self):
        """
        To create a new bid you should post on /api/bid/. This post should contains a JSON with the miniumum
        required fields.
        """

        response = self.client.post('/api/bids/',
                                    json.dumps({
                                        "title": "Ma première annonce wouhouhou test 1234",
                                        "description": 'Ceci est une description',
                                        "type": "OFFER"
                                    }),
                                    content_type="application/json; charset=utf-8")
        bids = Bid.objects.all()
        self.assertEquals(len(bids), 1)
        self.assertEquals(u'Ma première annonce wouhouhou test 1234', bids[0].title)
        self.assertEquals(201, response.status_code)
