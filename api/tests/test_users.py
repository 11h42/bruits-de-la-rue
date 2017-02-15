import json

from django.test.testcases import TestCase

from core.tests import factories


class UsersTest(TestCase):
    def setUp(self):
        self.address = factories.AddressFactory()
        self.address2 = factories.AddressFactory.create(title='Maison')
        self.user = factories.UserFactory.create(address=[self.address, self.address2])
        self.user2 = factories.UserFactory.create(address=[self.address, self.address2])
        self.association = factories.AssociationFactory(name="Association de jdupont", administrator=self.user)
        self.client.login(username=self.user.username, password="password")

    def test_create_new_address(self):
        address = {
            'title': 'Akema',
            'recipient_name': 'AKEMA SAS - Antoine Briand',
            'address1': '3 chemins de marticot',
            'address2': '',
            'zipcode': '33610',
            'town': 'CESTAS'
        }
        response = self.client.post('/api/addresses/?filter_by=current_user', json.dumps(address),
                                    content_type="application/json; charset=utf-8")
        self.assertEquals(201, response.status_code)

    def test_get_current_user_associations(self):
        response = self.client.get('/api/associations/?filter_by=current_user')
        self.assertEquals(200, response.status_code)
        self.assertTrue(response.content)
        self.assertEquals({u'associations': [self.association.serialize()]},
                          json.loads(response.content.decode('utf-8')))

    def test_get_user(self):
        response = self.client.get('/api/users/' + str(self.user2.id) + '/')
        self.assertEquals(405, response.status_code)
