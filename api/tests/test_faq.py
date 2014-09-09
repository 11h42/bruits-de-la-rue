import json

from django.test.testcases import TestCase

from core.tests import factories


class TestFaq(TestCase):
    def test_get_all_faq(self):
        faq = factories.FaqFactory()
        response = self.client.get('/api/faq/')
        self.assertEquals(200, response.status_code)
        self.assertEquals({u'faqs': [{u'answer': u'Factored answer', u'question': u'Factored question'}]},
                          json.loads(response.content))