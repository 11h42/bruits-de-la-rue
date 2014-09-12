from django.test.testcases import TestCase


# todo : Useless : Find how to test upload file / get files
class TestImageNoLogged(TestCase):
    def test_post_an_image_no_logged_returns_403(self):
        response = self.client.post('/api/images/', {})
        self.assertEquals(401, response.status_code)