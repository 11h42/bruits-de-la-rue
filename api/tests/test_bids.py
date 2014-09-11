# -*- coding: utf-8 -*-
import json

from django.test import TestCase

from api import constants

from core.models import Bid, StatusBids
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
        self.user_address = factories.AddressFactory(title="Adresse de test")
        self.user = factories.UserFactory(address=[self.user_address])
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
        self.assertEquals(returned_bid['type'], 'SUPPLY')
        self.assertEquals(returned_bid['current_user_id'], self.user.id)
        self.assertEquals(returned_bid['current_user_is_staff'], self.user.is_staff)
        self.assertEquals(200, response.status_code)

    def test_post_a_bid_with_all_required_fields(self):
        response = self.client.post('/api/bids/',
                                    json.dumps({
                                        "title": "Ma première annonce wouhouhou test 1234",
                                        "description": 'Ceci est une description',
                                        "type": "SUPPLY",
                                        'real_author': 'Jean Dupont',
                                    }),
                                    content_type="application/json; charset=utf-8")
        bids = Bid.objects.all()
        self.assertEquals(len(bids), 1)
        self.assertEquals(u'Ma première annonce wouhouhou test 1234', bids[0].title)
        self.assertEquals(201, response.status_code)

    def test_post_a_bid_that_start_tomorrow_and_have_the_status_on_hold(self):
        response = self.client.post('/api/bids/',
                                    json.dumps({
                                        "title": "Ma première annonce wouhouhou test 1234",
                                        "description": 'Ceci est une description',
                                        "type": "SUPPLY",
                                        'real_author': 'Jean Dupont',
                                        'begin': constants.TOMORROW_ISO,
                                        'end': constants.AFTER_TOMORROW_ISO
                                    }),
                                    content_type="application/json; charset=utf-8")
        bids = Bid.objects.all()
        self.assertEquals(len(bids), 1)
        self.assertEquals(u'Ma première annonce wouhouhou test 1234', bids[0].title)
        self.assertEquals(StatusBids.ONHOLD, bids[0].status_bid)
        self.assertEquals(201, response.status_code)

    def test_post_a_bid_with_all_authorized_fields(self):
        category = factories.BidCategoryFactory()
        bid = {'title': 'My bid',
               'description': 'The bid description',
               'type': 'SUPPLY',
               'real_author': 'Jean Dupont',
               'category': {'id': category.id, 'name': category.name},
               'quantity': 2,
               'localization': self.user_address.serialize()}
        response = self.client.post('/api/bids/', json.dumps(bid), content_type="application/json; charset=utf-8")
        bid = Bid.objects.get(title=bid['title'])
        self.assertEquals(201, response.status_code)
        self.assertEquals(u'My bid', bid.title)

    def test_accept_all_the_bid(self):
        creator = factories.UserFactory(username='bid creator')
        purchaser = self.user
        bid = factories.BidFactory(creator=creator, status_bid=StatusBids.RUNNING, quantity=120)
        bid_accept = {
            'id': bid.id,
            'title': bid.title,
            'description': bid.description,
            'creator': bid.creator.id,
            'status_bid': {'name': StatusBids.ACCEPTED},
            'purchaser': purchaser.id,
            'quantity': 120

        }
        response = self.client.put('/api/bids/%s/accept/' % bid.id, json.dumps(bid_accept))
        self.assertEquals(200, response.status_code)

        bid_accepted = Bid.objects.get(id=bid.id)
        self.assertEquals(StatusBids.ACCEPTED, bid_accepted.status_bid)
        self.assertEquals(self.user, bid_accepted.purchaser)

    def test_accept_bid_with_negative_value(self):
        creator = factories.UserFactory(username='bid creator')
        purchaser = self.user
        bid = factories.BidFactory(creator=creator, status_bid=StatusBids.RUNNING, quantity=120)
        bid_accept = {
            'id': bid.id,
            'title': bid.title,
            'description': bid.description,
            'creator': bid.creator.id,
            'status_bid': {'name': StatusBids.ACCEPTED},
            'purchaser': purchaser.id,
            'quantity': -120

        }
        response = self.client.put('/api/bids/%s/accept/' % bid.id, json.dumps(bid_accept))
        bid_non_accepted = Bid.objects.get(id=bid.id)
        self.assertEquals(StatusBids.RUNNING, bid_non_accepted.status_bid)
        self.assertEquals(bid.purchaser, None)
        self.assertEquals(120, bid_non_accepted.quantity)
        self.assertEquals(400, response.status_code)

    def test_accept_a_bid_that_have_no_quantity(self):
        creator = factories.UserFactory(username='bid creator')
        purchaser = self.user
        bid = factories.BidFactory(creator=creator, status_bid=StatusBids.RUNNING)
        bid_accept = {
            'id': bid.id,
            'status_bid': {'name': StatusBids.ACCEPTED},
        }
        response = self.client.put('/api/bids/%s/accept/' % bid.id, json.dumps(bid_accept))
        self.assertEquals(200, response.status_code)

        bid_accepted = Bid.objects.get(id=bid.id)
        self.assertEquals(StatusBids.ACCEPTED, bid_accepted.status_bid)
        self.assertEquals(self.user, bid_accepted.purchaser)

    def test_cant_accept_bid_that_belong_to_the_user(self):
        bid = factories.BidFactory(creator=self.user, quantity=120)
        bid_accept = {
            'id': bid.id,
            'title': bid.title,
            'description': bid.description,
            'creator': bid.creator.username,
            'status_bid': {'name': StatusBids.ACCEPTED},
            'purchaser': self.user.id,
            'quantity': 120

        }
        response = self.client.put('/api/bids/%s/accept/' % bid.id, json.dumps(bid_accept))
        self.assertEquals(400, response.status_code)
        self.assertEquals('{"message": "Vous ne pouvez accepter votre propre annonce", "code": 10217}',
                          response.content)

        bid_non_modified = Bid.objects.get(id=bid.id)
        self.assertEquals(StatusBids.RUNNING, bid_non_modified.status_bid)
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

    def test_update_bid(self):
        bid = factories.BidFactory(creator=self.user, status_bid=StatusBids.RUNNING)
        bid_updated = {
            'id': bid.id,
            'title': 'Nouveau titre',
            'description': bid.description,
            'type': bid.type,
            'real_author': 'toto'
        }
        response = self.client.put('/api/bids/%s/' % bid.id, json.dumps(bid_updated))
        self.assertEquals(200, response.status_code)
        bid_updated = Bid.objects.get(id=bid.id)
        self.assertEquals(bid_updated.title, 'Nouveau titre')

    def test_update_bid_passing_creator_does_not_change_creator(self):
        bid = factories.BidFactory(creator=self.user, status_bid=StatusBids.RUNNING)
        fakeCreator = factories.UserFactory(username='fakeCreator')
        bid_updated = {
            'id': bid.id,
            'title': 'Nouveau titre',
            'description': bid.description,
            'creator': fakeCreator.id,
            'type': 'SUPPLY'

        }
        response = self.client.put('/api/bids/%s/' % bid.id, json.dumps(bid_updated))
        update_bid = Bid.objects.get(id=bid.id)
        self.assertNotEqual(fakeCreator, update_bid.creator)
        self.assertEquals(400, response.status_code)


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
        self.assertEquals(bids[0]['real_author'], 'Jean Dupont')

    def test_post_a_bid_with_minimum_info_and_return_201(self):
        """
        To create a new bid you should post on /api/bid/. This post should contains a JSON with the miniumum
        required fields.
        """

        response = self.client.post('/api/bids/',
                                    json.dumps({
                                        "title": "Ma première annonce wouhouhou test 1234",
                                        "description": 'Ceci est une description',
                                        "type": "OFFER",
                                        'real_author': 'Jean Dupont',
                                    }),
                                    content_type="application/json; charset=utf-8")
        bids = Bid.objects.all()
        self.assertEquals(len(bids), 1)
        self.assertEquals(u'Ma première annonce wouhouhou test 1234', bids[0].title)
        self.assertEquals(201, response.status_code)

    def test_post_a_bid_with_its_association(self):
        """
        To create a new bid you should post on /api/bid/. This post should contains a JSON with the miniumum
        required fields.
        """
        association = factories.AssociationFactory(name="bid association")
        response = self.client.post('/api/bids/',
                                    json.dumps({
                                        "title": "Ma première annonce wouhouhou test 1234",
                                        "description": 'Ceci est une description',
                                        "type": "OFFER",
                                        'real_author': 'Jean Dupont',
                                        'association': association.serialize()
                                    }),
                                    content_type="application/json; charset=utf-8")
        bids = Bid.objects.all()
        self.assertEquals(len(bids), 1)
        self.assertEquals(u'Ma première annonce wouhouhou test 1234', bids[0].title)
        self.assertEquals(201, response.status_code)



