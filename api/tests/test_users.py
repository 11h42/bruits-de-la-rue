import json

from django.test.testcases import TestCase

from core.tests import factories


class UsersTest(TestCase):
    def setUp(self):
        self.address = factories.AddressFactory()
        self.address2 = factories.AddressFactory.create(title='Maison')
        self.association = factories.AssociationFactory(name="Association de jdupont")
        self.user = factories.UserFactory.create(username='jdupont', address=[self.address, self.address2],
                                                 associations=[self.association])
        self.client.login(username=self.user.username, password="password")

    def test_get_current_user_username(self):
        response = self.client.get('/api/users/current/')
        self.assertEquals(response.content, self.user.username)

    def test_get_current_user_address(self):
        self.maxDiff = None
        response = self.client.get('/api/users/current/address/')
        self.assertEquals(200, response.status_code)

    def test_create_new_address(self):
        address = {
            'title': 'Akema',
            'recipient_name': 'AKEMA SAS - Antoine Briand',
            'address1': '3 chemins de marticot',
            'address2': '',
            'zipcode': '33610',
            'town': 'CESTAS'
        }
        response = self.client.post('/api/users/current/address/', json.dumps(address),
                                    content_type="application/json; charset=utf-8")
        self.assertEquals(201, response.status_code)

    def test_get_current_user_associations(self):
        response = self.client.get('/api/users/current/associations/')
        self.assertEquals(200, response.status_code)
        self.assertTrue(response.content)
        self.assertEquals({u'associations': [{u'fax': u'0987654321', u'name': u'Association de jdupont',
                                              u'url_site': u'association-lambda.com',
                                              u'email': u'contact@association-lambda.com', u'phone': u'0123456789',
                                              u'address': None, u'id': self.association.id}]},
                          json.loads(response.content))