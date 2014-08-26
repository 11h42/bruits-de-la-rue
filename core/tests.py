from datetime import datetime
from datetime import timedelta
from django.test import TestCase

from api.tests import factories
from core import views
from core.models import clean_serialize


class TestBids(TestCase):
    def test_clean_serialize(self):
        begin = datetime.today()
        end = begin + timedelta(days=2)
        data = {'end': end, 'begin': begin}
        cleaned_serialize = clean_serialize(data)
        self.assertEquals(cleaned_serialize['end'], data['end'])
        self.assertEquals(cleaned_serialize['begin'], data['begin'])
        self.assertEquals(cleaned_serialize['time_left'], str(end - begin))


class UserTest(TestCase):
    def test_function_return_email_if_username_with_non_existing_username(self):
        self.assertEquals(views.return_email_if_username("abriand1456"), None)

    def test_function_return_email_if_username_with_existing_username(self):
        self.user = factories.UserFactory(username="abriand", email="abriand@akema.fr")
        self.assertEquals(views.return_email_if_username("abriand"), self.user.email)

    def test_function_return_email_if_username_with_good_email(self):
        self.assertEquals(views.return_email_if_username("abriand@akema.fr"), "abriand@akema.fr")

    def test_function_return_email_if_username_with_bad_email(self):
        self.assertEquals(views.return_email_if_username("abri@and@akema.fr"), None)
