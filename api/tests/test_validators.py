# -*- coding: utf-8 -*-
import datetime

from django.test import TestCase

from api.validators import BidValidator


class TestValidators(TestCase):
    def setUp(self):
        self.bid_validator = BidValidator()

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
            "quantity": ""}
        ))