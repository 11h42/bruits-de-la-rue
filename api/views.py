# coding=utf-8
import json

from django.http.response import HttpResponse

from api.decorators import b2rue_authenticated as is_authenticated
from api.decorators import catch_any_unexpected_exception
from api.errors import error_codes
from api.http_response import HttpMethodNotAllowed, HttpCreated, HttpBadRequest
from api.validators import BidValidator
from core.models import Bid, BidCategories


def get_bids(request):
    bids = Bid.objects.filter(status="RUNNING")
    return_bids = []
    if bids:
        for bid in bids:
            return_bids.append(bid.serialize())
    return HttpResponse(json.dumps({'bids': return_bids}), content_type='application/json')


def create_bid(request):
    bid = json.loads(request.body)

    if bid:
        bid_validator = BidValidator()
        if bid_validator.bid_is_valid(bid):
            bid['creator'] = request.user
            if 'category' in bid:
                bid['category'], created = BidCategories.objects.get_or_create(name=bid['category'])
            new_bid = Bid(**bid)
            new_bid.save()
            new_bid_id = new_bid.id
            return HttpCreated(json.dumps({'bid_id': new_bid_id}), location='/api/bids/%d/' % new_bid_id)
    return HttpBadRequest(10900, error_codes['10900'])


def get_bid(request, bid_id):
    bids = Bid.objects.filter(id=bid_id)
    if bids:
        return HttpResponse(json.dumps(bids[0].serialize()), content_type='application/json')


def accept_bid(request, bid_id):
    bids = Bid.objects.filter(id=bid_id)
    if bids:
        bid = bids[0]
        user = request.user
        if user != bid.creator and bid.status == "RUNNING":
            bid.purchaser = user
            bid.status = "ACCEPTED"
            bid.save()
            return HttpResponse()
    return HttpMethodNotAllowed()


@is_authenticated
@catch_any_unexpected_exception
def handle_bids(request):
    if request.method == "GET":
        return get_bids(request)

    if request.method == "POST":
        return create_bid(request)
    return HttpMethodNotAllowed()


@is_authenticated
@catch_any_unexpected_exception
def handle_bid(request, bid_id):
    if request.method == 'GET':
        return get_bid(request, bid_id)
    if request.method == 'PUT':
        return accept_bid(request, bid_id)
    return HttpMethodNotAllowed()


def get_available_categories(request):
    categories = BidCategories.objects.all()
    return_categories = []
    if categories:
        for category in categories:
            return_categories.append(category.serialize())
    return HttpResponse(json.dumps({'categories': return_categories}), content_type='application/json')


@is_authenticated
@catch_any_unexpected_exception
def handle_categories(request):
    if request.method == "GET":
        return get_available_categories(request)
    return HttpMethodNotAllowed()