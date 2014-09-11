# coding=utf-8
from api import constants
from core.models import BidCategory, Address, Association, StatusBids


class BidValidator(object):
    def __init__(self, json_bid):
        self.bid = json_bid
        self.error_message = ''
        self.error_code = 10666

    def get_bid_object(self, user):
        if 'begin' in self.bid and self.bid['begin'] > constants.TODAY_ISO:
            self.bid['status_bid'] = StatusBids.ONHOLD
        self.bid['creator'] = user
        if 'category' in self.bid:
            self.bid['category'] = BidCategory.objects.get(id=self.bid['category']['id'])
        if 'localization' in self.bid:
            self.bid['localization'] = Address.objects.get(id=self.bid['localization']['id'])
        if 'association' in self.bid:
            self.bid['association'] = Association.objects.get(id=self.bid['association']['id'])
        return self.bid

    def is_valid(self):
        """
        return true if a given self.bid is valid
        :param self.bid:
        :return: True if all the rules are respected. False instead.
        """
        required_fields = ['title', 'description', 'type', 'real_author']
        authorized_fields = required_fields + ['begin', 'end', 'category', 'quantity', 'id', 'localization',
                                               'status_bid', 'association']
        if not self.bid:
            self.error_message = u'Erreur: Veillez à bien remplir tous les champs'
            return False

        for key, value in self.bid.items():
            if key not in authorized_fields:
                self.error_message = u'Le champs %s est invalide' % key

        for fields in required_fields:
            if fields not in self.bid:
                self.error_message = u'key %s is required' % fields

        if 'begin' in self.bid and 'end' in self.bid and self.bid['end']:
            if self.bid['begin'] > self.bid['end']:
                self.error_message = u'Erreur : La date de début doit être strictement inférieur à la date de fin'

        if 'begin' in self.bid:
            if self.bid['begin'] < constants.TODAY_ISO:
                self.error_message = u'Erreur : La date de début doit être supérieure ou égale à la date du jour'

        return len(self.error_message) == 0