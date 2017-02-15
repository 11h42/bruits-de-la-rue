import json

from django.test import TestCase

from core.models import Bid, StatusBids
from core.tests import factories


class TestBidsApi(TestCase):
    def setUp(self):
        self.user = factories.UserFactory()
        self.client.login(username=self.user.username, password="password")

    def test_get_bids_empty(self):
        response = self.client.get('/api/bids/')
        self.assertEquals(200, response.status_code)
        bids = json.loads(response.content.decode('utf-8'))['bids']
        self.assertEquals(bids, [])

    def test_get_bids_with_parameters(self):
        response = self.client.get('/api/bids/?order_by=end&limit=1000')
        self.assertEquals(200, response.status_code)
        bids = json.loads(response.content.decode('utf-8'))['bids']
        self.assertEquals(bids, [])

    def test_get_bids_200(self):
        bid = factories.BidFactory(creator=self.user)
        response = self.client.get('/api/bids/')
        self.assertEquals(200, response.status_code)
        bids = json.loads(response.content.decode('utf-8'))['bids']
        self.assertEquals(len(bids), 1)
        self.assertEquals(bids[0]['id'], bid.id)
        self.assertEquals(bids[0]['title'], 'Annonce de test')
        self.assertEquals(bids[0]['real_author'], 'Jean Dupont')

    def test_get_bids_return_every_running_bids_or_own_bids(self):
        factories.BidFactory.create(title='bid 1', status_bid=StatusBids.ONHOLD,
                                    creator=factories.UserFactory(is_public_member=True))
        factories.BidFactory(title='bid 2', status_bid=StatusBids.ONHOLD, creator=self.user)
        factories.BidFactory(title='bid 3', status_bid=StatusBids.RUNNING, creator=self.user)
        response = self.client.get('/api/bids/')
        self.assertEquals(200, response.status_code)
        bids = json.loads(response.content.decode('utf-8'))['bids']
        self.assertEquals(len(bids), 2)
        self.assertEquals(bids[0]['title'], 'bid 2')

    def test_post_a_bid_with_minimum_info_and_return_201(self):
        response = self.client.post('/api/bids/',
                                    json.dumps({
                                        "title": "Ma première annonce wouhouhou test 1234",
                                        "type": "OFFER",
                                        'real_author': 'Jean Dupont',
                                    }),
                                    content_type="application/json; charset=utf-8")
        bids = Bid.objects.all()
        self.assertEquals(len(bids), 1)
        self.assertEquals(u'Ma première annonce wouhouhou test 1234', bids[0].title)
        self.assertEquals(201, response.status_code)

    def test_post_a_bid_with_unit(self):
        response = self.client.post('/api/bids/',
                                    json.dumps({
                                        "title": "Ruban rouge",
                                        "type": "OFFER",
                                        'real_author': 'Jean Dupont',
                                        "quantity": 12,
                                        "unit": "metre"
                                    }),
                                    content_type="application/json; charset=utf-8")
        bids = Bid.objects.all()
        self.assertEquals(u'metre', bids[0].unit)
        self.assertEquals(201, response.status_code)


class TestBidsPublicMemberApi(TestCase):
    def setUp(self):
        self.user = factories.UserFactory(is_public_member=True)
        self.client.login(username=self.user.username, password="password")

    def test_post_a_bid_with_user_public_set_status_to_onhold(self):
        self.client.post('/api/bids/',
                         json.dumps({
                             "title": "Ma première annonce wouhouhou test 1234",
                             "type": "OFFER",
                             'real_author': 'Jean Dupont',
                         }),
                         content_type="application/json; charset=utf-8")
        bids = Bid.objects.all()
        self.assertEquals(StatusBids.ONHOLD, bids[0].status_bid)


class TestBidsAdminApi(TestCase):
    def setUp(self):
        self.user = factories.AdminFactory()
        self.client.login(username=self.user.username, password="password")

    def test_admin_get_every_bids(self):
        factories.BidFactory.create(title='bid 1', status_bid=StatusBids.ONHOLD,
                                    creator=factories.UserFactory(is_public_member=True))
        factories.BidFactory(title='bid 2', status_bid=StatusBids.RUNNING,
                             creator=factories.UserFactory(is_public_member=False))
        response = self.client.get('/api/bids/')
        self.assertEquals(200, response.status_code)
        bids = json.loads(response.content.decode('utf-8'))['bids']
        self.assertEquals(len(bids), 2)
