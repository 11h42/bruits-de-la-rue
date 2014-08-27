from datetime import datetime
from datetime import timedelta

from django.test import TestCase

from core.models import clean_serialize


class TestBids(TestCase):
    def test_clean_serialize(self):
        #todo rename this test
        begin = datetime.today()
        end = begin + timedelta(days=2)
        data = {'end': end, 'begin': begin}
        cleaned_serialize = clean_serialize(data)
        self.assertEquals(cleaned_serialize['end'], data['end'])
        self.assertEquals(cleaned_serialize['begin'], data['begin'])
        self.assertEquals(cleaned_serialize['time_left'], str(end - begin))


