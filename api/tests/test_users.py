import json

from django.test.testcases import TestCase

from core.tests import factories


class UsersTest(TestCase):
    def setUp(self):
        self.address = factories.AddressFactory()
        self.address2 = factories.AddressFactory(title='Maison')
        self.user = factories.UserFactory.create(username='jdupont', address=[self.address])
        self.client.login(username=self.user.username, password="password")

    def test_get_current_user_username(self):
        response = self.client.get('/api/users/current/')
        self.assertEquals(response.content, self.user.username)

    def test_get_current_user_address(self):
        response = self.client.get('/api/users/current/address')
        address_returned = json.loads(response.content)
        self.assertEquals(200, response.status_code)
        self.assertEquals(address_returned, {})
