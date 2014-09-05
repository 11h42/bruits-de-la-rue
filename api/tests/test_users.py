import json

from django.test.testcases import TestCase

from core.tests import factories


class UsersTest(TestCase):
    def setUp(self):
        self.address = factories.AddressFactory()
        self.address2 = factories.AddressFactory(title='Maison')
        self.user = factories.UserFactory.create(username='jdupont', address=[self.address, self.address2])
        self.client.login(username=self.user.username, password="password")

    def test_get_current_user_username(self):
        response = self.client.get('/api/users/current/')
        self.assertEquals(response.content, self.user.username)

    def test_get_current_user_address(self):
        response = self.client.get('/api/users/current/address/')
        address_returned = json.loads(response.content)
        self.assertEquals(200, response.status_code)
        self.assertEquals(address_returned, {"address": [
            {"town": "Cestas", "title": "Akema", "address1": "3 chemin de marticot", "address2": None, "zipcode": 33610,
             "recipient_name": "Akema", "id": 1}]})

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
