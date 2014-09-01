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
        categories_returned = json.loads(response.content)['categories']

        if categories_returned:
            for category_returned in categories_returned:
                self.assertEquals(category_returned['name'], category.name)
                self.assertTrue('name' in category_returned)