from django.test.testcases import TestCase

from core.tests import factories


class AssociationTestCase(TestCase):
    def test_association_to_json_method(self):
        user = factories.UserFactory()
        self.client.login(username=user.username, password="password")
        association = factories.AssociationFactory(name="toto")
        expected_association = {'id': association.id, 'name': association.name, 'address': association.address,
                                'phone': association.phone, 'url_site': association.url_site,
                                'email': association.email, 'administrator': association.administrator.serialize()}
        self.assertDictEqual(association.serialize(), expected_association)
