# -*- coding: utf-8 -*-
import datetime

from django.test import TestCase

from api.validators import BidValidator
from core.tests import factories


class TestValidators(TestCase):
    def setUp(self):
        self.bid_validator = BidValidator()
        self.creator = factories.UserFactory()

    def test_bid_validor_is_not_valid(self):
        self.assertFalse(self.bid_validator.bid_is_valid({}))
        self.assertFalse(self.bid_validator.bid_is_valid({'description': ""}))
        self.assertFalse(self.bid_validator.bid_is_valid({'title': "Toto",
                                                          'description': "Titi",
                                                          "toto": "tata"}))

    def test_bid_validator_with_bad_date(self):
        today = datetime.datetime.today()
        yesterday = today - datetime.timedelta(days=1)
        bid_with_bad_date = {"title": "Ma première annonce wouhouhou test 1234",
                             "description": 'Ceci est une description',
                             "type": "DEMAND",
                             "begin": today.isoformat(),
                             "end": yesterday.isoformat()}
        self.assertFalse(self.bid_validator.bid_is_valid(bid_with_bad_date))

    def test_bid_is_valid(self):
        today = datetime.datetime.today()
        tomorrow = today + datetime.timedelta(days=1)
        self.assertTrue(self.bid_validator.bid_is_valid({
            'title': "Chaise",
            'description': "Un siège, un dossier, 4 pieds",
            'type': 'Offer',
            'category': 'ALIMENTAIRE',
            "begin": today.isoformat(),
            "end": tomorrow.isoformat(),
            "quantity": "",
            "real_author": "titi"}
        ))

    def test_bids_are_the_same(self):
        self.assertTrue(self.bid_validator.bid_are_the_same(
            {'begin': None, 'description': 'BID UNIQUE UNIQUE UNIQUE',
             'creator': 'test',
             'status_bid': u'EN COURS',
             'real_author': 'Jean Dupont',
             'association': {'fax': '0987654321', 'name': 'Association Lambda', 'url_site': 'association-lambda.com',
                             'email': 'contact@association-lambda.com', 'phone': '0123456789', 'address': None,
                             'id': 1},
             'category': None,
             'end': None,
             'title': 'Annonce de test',
             'localization': None,
             'id': 1,
             'type': 'SUPPLY',
             'quantity': None},
            {'begin': None, 'description': 'BID UNIQUE UNIQUE UNIQUE',
             'creator': 'test',
             'status_bid': u'EN COURS',
             'real_author': 'Jean Dupont',
             'association': {'fax': '0987654321', 'name': 'Association Lambda', 'url_site': 'association-lambda.com',
                             'email': 'contact@association-lambda.com', 'phone': '0123456789', 'address': None,
                             'id': 1},
             'category': None,
             'end': None,
             'title': 'Annonce de test',
             'localization': None,
             'id': 1,
             'type': 'SUPPLY',
             'quantity': None}))

    def test_bids_are_not_the_same(self):
        bid1 = factories.BidFactory(creator=self.creator)
        bid2 = factories.BidFactory(creator=self.creator, description='Not the same !')
        self.assertFalse(self.bid_validator.bid_are_the_same(bid1.serialize(), bid2.serialize()))
