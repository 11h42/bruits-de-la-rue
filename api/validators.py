# coding=utf-8
class BidValidator(object):
    @staticmethod
    def bid_is_valid(bid):
        """
        return true if a given bid is valid
        :param bid:
        :return: True if all the rules are respected. False instead.
        """
        required_fields = ['title', 'description', 'type', 'real_author']
        authorized_fields = required_fields + ['begin', 'end', 'category', 'quantity', 'id', 'localization', 'status_bid',
                                               'association']
        errors = []
        if bid:
            for key, value in bid.items():
                if key not in authorized_fields:
                    errors.append(u'Le champs %s est invalide' % key)

            for fields in required_fields:
                if fields not in bid:
                    errors.append(u'key %s is required' % fields)

            if 'begin' in bid and 'end' in bid:
                if bid['begin'] > bid['end']:
                    errors.append(u'Erreur : La date de début doit être strictement inférieur à la date de fin')
        else:
            errors.append(u'Erreur: Veillez à bien remplir tous les champs')
        return len(errors) == 0