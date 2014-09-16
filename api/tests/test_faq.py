import json

from django.test.testcases import TestCase

from core.models import Faq

from core.tests import factories


class TestFaq(TestCase):
    def setUp(self):
        user = factories.UserFactory()
        self.client.login(username=user.username, password="password")

    def test_get_all_faq(self):
        factories.FaqFactory()
        response = self.client.get('/api/faq/')
        self.assertEquals(200, response.status_code)
        self.assertEquals({u'faqs': [{u'id': 2, u'answer': u'Factored answer', u'question': u'Factored question'}]},
                          json.loads(response.content))

    def test_add_faq_without_staff_account(self):
        faq = {'question': 'Combien font 2 + 2 ?',
               'answer': '4'}
        response = self.client.post('/api/faq/', json.dumps(faq), content_type="application/json; charset=utf-8")
        self.assertEquals(403, response.status_code)

    def test_delete_faq_without_staff_account(self):
        faq = factories.FaqFactory()
        response = self.client.delete('/api/faq/%s/' % faq.id)
        self.assertEquals(403, response.status_code)
        self.assertTrue(bool(Faq.objects.all()))


class TestFaqWithStaffUser(TestCase):
    def setUp(self):
        self.user = factories.UserFactory(is_staff=True)
        self.client.login(username=self.user.username, password="password")

    def test_add_faq(self):
        faq = {'question': 'Combien font 2 + 2 ?',
               'answer': '4'}
        response = self.client.post('/api/faq/', json.dumps(faq), content_type="application/json; charset=utf-8")
        self.assertEquals(201, response.status_code)
        faq_created = Faq.objects.all()
        self.assertTrue(faq_created)

    def test_delete_faq(self):
        faq = factories.FaqFactory()
        response = self.client.delete('/api/faq/%s/' % faq.id)
        self.assertEquals(200, response.status_code)
        self.assertFalse(bool(Faq.objects.all()))