# -*- coding: utf-8 -*-
import json

from django.test import TestCase
from api.tests import factories

from api.tests.factories import BidFactory


class TestBids(TestCase):
    def setUp(self):
        self.user = factories.UserFactory.create(email="toto@titi.com", password="1234")
        self.bid = BidFactory(name='test name', caller=self.user)

    def test_get_bids_non_logged(self):
        response = self.client.get('/api/bids/')
        self.assertEquals(302, response.status_code)

    def test_get_bids_logged(self):
        login = self.client.login(username=self.user.email, password="1234")
        self.assertTrue(login)

        response = self.client.get('/api/bids/')
        self.assertEquals(200, response.status_code)
        bids = json.loads(response.content)['bids']
        self.assertEquals(bids[0]['id'], self.bid.id)
        self.assertEquals(bids[0]['name'], 'test name')
        self.assertEquals(len(bids), 1)














        # def test_get_non_existing_bid(self):
        # response = self.client.get(reverse('api:get-bid', kwargs={'bid_id': 4}))
        # self.assertEquals(400, response.status_code)
        #
        # def test_post_bid(self):
        # user = UserFactory(email="abriand@toto.com", password="toto")
        # bid_category = factories.BidCategoryFactory()
        #     emergency = factories.EmergencyLevelFactory()
        #     login = self.client.login(username=user.email, password="toto")
        #
        #     response = self.client.post(reverse('api:post-bid'),
        #                                 json.dumps({
        #                                     'caller': user.id,
        #                                     'name': "Fruits et légumes",
        #                                     'acceptor': "",
        #                                     'begin': str(datetime.today()),
        #                                     'end': str(datetime.today() + timedelta(days=2)),
        #                                     'quantity': str(12),
        #                                     'adress1': "Rue de la petite avenue",
        #                                     'adress2': "",
        #                                     'zipcode': "33000",
        #                                     'town': "Bordeaux",
        #                                     'country': "France",
        #                                     'real_author': "abriand",
        #                                     'description': "Ceci est une description",
        #                                     'bidCategory': bid_category.bid_category_name,
        #                                     'photo': '/images/default.png',
        #                                     'quantity_type': 'KG',
        #                                     'status': 'Ouvert',
        #                                     'type': 'Offre',
        #                                     'emergency_level_level': emergency.level
        #                                 }),
        #                                 content_type='application/json')
        #     self.assertEquals(response.status_code, 200)
        #     bid_created = Bid.objects.filter(name="Fruits et légumes")[:1]
        #     self.assertTrue(bool(bid_created))
        #
        # def test_post_bid_non_logged_in(self):
        #     response = self.client.post(reverse('api:post-bid'))
        #     self.assertEquals(response.status_code, 302)

