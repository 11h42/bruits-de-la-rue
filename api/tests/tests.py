# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from api.tests import factories

from api.tests.factories import BidFactory, UserFactory
from core.models.models import Bid


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

    def test_post_bid(self):
        user = UserFactory(email="abriand@toto.com", password="toto")
        bid_category = factories.BidCategoryFactory()
        emergency = factories.EmergencyLevelFactory()
        login = self.client.login(username=user.email, password="toto")

        response = self.client.post(reverse('api:post-bid'),
                                    json.dumps({
                                        'caller': user.id,
                                        'name': "Fruits et légumes",
                                        'acceptor': "",
                                        'begin': str(datetime.today()),
                                        'end': str(datetime.today() + timedelta(days=2)),
                                        'quantity': str(12),
                                        'adress1': "Rue de la petite avenue",
                                        'adress2': "",
                                        'zipcode': "33000",
                                        'town': "Bordeaux",
                                        'country': "France",
                                        'real_author': "abriand",
                                        'description': "Ceci est une description",
                                        'bidCategory': bid_category.bid_category_name,
                                        'photo': '/images/default.png',
                                        'quantity_type': 'KG',
                                        'status': 'Ouvert',
                                        'type': 'Offre',
                                        'emergency_level_name': emergency.name,
                                        'emergency_level_level': emergency.level
                                    }),
                                    content_type='application/json')
        self.assertEquals(response.status_code, 200)
        bid_created = Bid.objects.filter(name="Fruits et légumes")[:1]
        self.assertTrue(bool(bid_created))

    def test_post_bid_non_logged_in(self):
        response = self.client.post(reverse('api:post-bid'))
        self.assertEquals(response.status_code, 302)

