import json

from django.test.testcases import TestCase

from core.tests import factories


class TestAssociations(TestCase):
    def setUp(self):
        user = factories.UserFactory()
        self.client.login(username=user.username, password="password")

    def test_get_all_associations(self):
        association = factories.AssociationFactory()
        response = self.client.get('/api/associations/')
        self.assertEquals(200, response.status_code)
        self.assertEquals({'associations': [association.serialize()]}, json.loads(response.content))

    def test_get_association(self):
        self.maxDiff = None
        association = factories.AssociationFactory()
        response = self.client.get('/api/associations/%s/' % association.id)
        self.assertEquals(200, response.status_code)
        self.assertEquals({'association': association.serialize(), 'members': []}, json.loads(response.content))