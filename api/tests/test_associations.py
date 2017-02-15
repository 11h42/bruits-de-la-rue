import json

from django.test import TestCase

from core.models import Association
from core.tests import factories


class TestAssociations(TestCase):
    def setUp(self):
        self.user = factories.UserFactory()
        self.client.login(username=self.user.username, password="password")

    def test_get_all_associations(self):
        association = factories.AssociationFactory(administrator=self.user)
        response = self.client.get('/api/associations/')
        self.assertEquals(200, response.status_code)
        self.assertEquals({'associations': [association.serialize()]}, json.loads(response.content.decode('utf-8')))


class TestFaqWithStaffUser(TestCase):
    def setUp(self):
        self.user = factories.UserFactory(is_staff=True)
        self.client.login(username=self.user.username, password="password")
        self.maxDiff = None

    def test_delete_association(self):
        association = factories.AssociationFactory(administrator=self.user)
        response = self.client.delete('/api/associations/%s/' % association.id)
        self.assertEqual(204, response.status_code)
        self.assertEqual(len(Association.objects.all()), 0)

    def test_get_association_with_user_is_staff(self):
        association = factories.AssociationFactory(administrator=self.user)
        response = self.client.get('/api/associations/%s/' % association.id)
        self.assertEquals(200, response.status_code)
        self.assertDictEqual({'association': association.serialize(True)},
                             json.loads(response.content.decode('utf-8')))

    def test_add_members_to_an_association(self):
        association = factories.AssociationFactory(administrator=self.user)
        self.assertEqual(len(association.members.all()), 0)
        new_user = factories.UserFactory(username='UserX')
        response = self.client.post('/api/associations/%s/members/%s/' % (association.id, new_user.id))
        self.assertEqual(201, response.status_code)
        association_updated = Association.objects.get(id=association.id)
        self.assertEqual(len(association_updated.members.all()), 1)
