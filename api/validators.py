# coding=utf-8

from core.models import BidCategory, Address, Association, StatusBids, Photo


class BidValidator(object):
    def __init__(self, json_bid):
        self.bid = json_bid
        self.error_message = ''
        self.error_code = 10666

    def get_bid_object(self, user):
        self.bid['creator'] = user
        if not 'status_bid' in self.bid or self.bid['status_bid'] is None:
            self.bid['status_bid'] = StatusBids.RUNNING
        if 'category' in self.bid and self.bid['category']:
            self.bid['category'] = BidCategory.objects.get(id=self.bid['category']['id'])
        if 'localization' in self.bid and self.bid['localization']:
            self.bid['localization'] = Address.objects.get(id=self.bid['localization']['id'])
        if 'association' in self.bid and self.bid['association']:
            self.bid['association'] = Association.objects.get(id=self.bid['association']['id'])
        if 'photo' in self.bid and self.bid['photo']:
            self.bid['photo'] = Photo.objects.get(id=self.bid['photo'])

        return self.bid

    def is_valid(self):
        """
        return true if a given self.bid is valid
        :param self.bid:
        :return: True if all the rules are respected. False instead.
        """
        required_fields = ['title', 'type']
        authorized_fields = required_fields + ['begin', 'description', 'end', 'category', 'quantity', 'id',
                                               'localization', 'status_bid', 'association', 'photo', 'creator',
                                               'real_author', 'unit']
        if not self.bid:
            self.error_message = u'Erreur: Veillez à bien remplir tous les champs'
            return False
        for key, value in self.bid.items():
            if key not in authorized_fields:
                self.error_message = u'Le champs %s est invalide' % key
        for fields in required_fields:
            if fields not in self.bid:
                self.error_message = u'le champ %s est obligatoire' % fields
            if 'title' not in self.bid or self.bid['title'] is None:
                self.error_message = u'Vous devez renseigner un titre pour votre annonce'
        if 'begin' in self.bid and self.bid['begin'] and 'end' in self.bid and self.bid['end']:
            if self.bid['begin'] > self.bid['end']:
                self.error_message = u'Erreur : La date de début doit être strictement inférieure à la date de fin'
        return len(self.error_message) == 0


class AddressValidator(object):
    def __init__(self, json_address):
        self.address = json_address
        self.error_message = ''
        self.error_code = 10666

    def is_valid(self):
        """
        return true if a given self.bid is valid
        :param self.bid:
        :return: True if all the rules are respected. False instead.
        """
        required_fields = ['title', 'town']
        authorized_fields = required_fields + ['address1', 'recipient_name', 'zipcode', 'address2']
        if not self.address:
            self.error_message = u'Erreur: Veillez à bien remplir tous les champs'
            return False
        for key, value in self.address.items():
            if key not in authorized_fields:
                self.error_message = u'Le champs %s est invalide' % key
        for fields in required_fields:
            if fields not in self.address or self.address[fields] is None:
                self.error_message = u'key %s is required' % fields
        return len(self.error_message) == 0
