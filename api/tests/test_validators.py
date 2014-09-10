# -*- coding: utf-8 -*-

from django.test import TestCase

from api.validators import BidValidator
from core.tests import factories
from api import constants


class TestValidators(TestCase):
    def setUp(self):
        self.creator = factories.UserFactory()

    def test_bid_validor_is_not_valid(self):
        self.assertFalse(BidValidator({}).is_valid())
        self.assertFalse(BidValidator({'description': ""}).is_valid())
        self.assertFalse(BidValidator({'title': "Toto",
                                       'description': "Titi",
                                       "toto": "tata"}).is_valid())

    def test_bid_validator_with_bad_date(self):
        bid_with_bad_date = {"title": "Ma première annonce wouhouhou test 1234",
                             "description": 'Ceci est une description',
                             "type": "DEMAND",
                             "begin": constants.TODAY_ISO,
                             "end": constants.YESTERDAY_ISO}
        self.assertFalse(BidValidator(bid_with_bad_date).is_valid())

    def test_bid_is_valid(self):
        self.assertTrue(BidValidator({
            'title': "Chaise",
            'description': "Un siège, un dossier, 4 pieds",
            'type': 'Offer',
            'category': 'ALIMENTAIRE',
            "begin": constants.TODAY_ISO,
            "end": constants.TOMORROW_ISO,
            "quantity": "",
            "real_author": "titi"}
        ).is_valid())