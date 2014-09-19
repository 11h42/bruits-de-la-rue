import json

from django.test.testcases import TestCase

from core.models import Association
from core.tests import factories


class TestAssociations(TestCase):
    def setUp(self):
        self.user = factories.UserFactory()
        self.client.login(username=self.user.username, password="password")

    def test_get_all_associations(self):
        association = factories.AssociationFactory()
        response = self.client.get('/api/associations/')
        self.assertEquals(200, response.status_code)
        self.assertEquals({'associations': [association.serialize()]}, json.loads(response.content))

    def test_get_association_with_user_administrator(self):
        association = factories.AssociationFactory(administrator=self.user)
        response = self.client.get('/api/associations/%s/' % association.id)
        self.assertEquals(200, response.status_code)
        self.assertEquals({'association': association.serialize(), 'members': []}, json.loads(response.content))

    def test_get_association_with_user_is_staff(self):
        self.client.logout()
        staff_user = factories.UserFactory(username='staff', is_staff=True)
        self.client.login(username=staff_user.username, password="password")
        association = factories.AssociationFactory()
        response = self.client.get('/api/associations/%s/' % association.id)
        self.assertEquals(200, response.status_code)
        self.assertEquals({'association': association.serialize(), 'members': []}, json.loads(response.content))

    def test_get_association_with_user_is_superuser(self):
        self.client.logout()
        superuser = factories.UserFactory(username='big boss', is_staff=True)
        self.client.login(username=superuser.username, password="password")
        association = factories.AssociationFactory()
        response = self.client.get('/api/associations/%s/' % association.id)
        self.assertEquals(200, response.status_code)
        self.assertEquals({'association': association.serialize(), 'members': []}, json.loads(response.content))

    def test_add_members_to_an_association(self):
        association = factories.AssociationFactory(members=[self.user], administrator=self.user)
        update_asso = {
            'name': 'Yeap',
            'members': [factories.UserFactory(username='UserX').id]
        }
        response = self.client.put('/api/associations/%s/' % association.id,
                                   json.dumps(update_asso))
        self.assertEqual(200, response.status_code)
        asso_updated = Association.objects.get(id=association.id)
        self.assertEqual(asso_updated.name, 'Yeap')
        self.assertEqual(len(asso_updated.members.all()), 2)

    def test_delete_association(self):
        association = factories.AssociationFactory(members=[self.user], administrator=self.user)
        response = self.client.delete('/api/associations/%s/' % association.id)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(Association.objects.all()), 0)