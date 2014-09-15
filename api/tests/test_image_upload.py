import json
import os

from django.core.files import File
from django.test.testcases import TestCase

from core.models import Photo

from core.tests import factories


class TestImageNoLogged(TestCase):
    def test_post_an_image_no_logged_returns_403(self):
        response = self.client.post('/api/images/', {})
        self.assertEquals(401, response.status_code)


class TestImageLogged(TestCase):
    def setUp(self):
        user = factories.UserFactory()
        self.client.login(username=user.username, password="password")
        self.file = File(
            open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'inputs', '5x5.png')))

    def test_post_an_image(self):
        response = self.client.post('/api/images/', {u'bid_image': self.file})
        photo = Photo.objects.all()
        self.assertEquals(1, len(photo))
        self.assertEquals(200, response.status_code)

    def test_get_an_image(self):
        photo = factories.PhotoFactory()
        response = self.client.get('/api/images/%s/' % photo.id)
        self.assertEquals(200, response.status_code)
        self.assertEquals(json.loads(response.content), {'url': photo.photo.url})

    def test_delete_photo(self):
        photo = factories.PhotoFactory()
        response = self.client.delete('/api/images/%s/' % photo.id)
        self.assertFalse(Photo.objects.all())
        self.assertEquals(200, response.status_code)