import json

from django.test import TestCase

from core.tests import factories


class CategoriesTest(TestCase):
    def setUp(self):
        self.user = factories.UserFactory()
        self.client.login(username=self.user.username, password="password")

    def test_get_categories_available(self):
        category = factories.BidCategoryFactory()

        response = self.client.get('/api/categories/')
        categories_returned = json.loads(response.content.decode('utf-8'))['categories']

        self.assertEquals(categories_returned[0]['id'], category.id)
        self.assertEquals(categories_returned[0]['name'], category.name)
        self.assertEqual(len(categories_returned), 1)