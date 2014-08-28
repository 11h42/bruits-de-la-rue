# coding=utf-8
import json

from django.http.response import HttpResponse

from api.decorators import b2rue_authenticated as is_authenticated
from api.decorators import catch_any_unexpected_exception
from api.errors import error_codes
from api.http_response import HttpMethodNotAllowed, HttpCreated, HttpBadRequest
from api.validators import BidValidator
from core.models import Bid


@is_authenticated
@catch_any_unexpected_exception
def get_bids(request):
    bids = Bid.objects.all()
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
            try:
                new_bid = Bid(**bid)
                new_bid.save()
                new_bid_id = new_bid.id
                return HttpCreated(json.dumps({'mailing_id': new_bid_id}), location='/api/bids/%d/' % new_bid_id)
            except Exception:
                raise
    return HttpBadRequest(10203, error_codes['10900'])


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

    return HttpMethodNotAllowed()


# todo test me
@is_authenticated
@catch_any_unexpected_exception
def get_bid(request, bid_id):
    bids = Bid.objects.filter(id=bid_id)
    return_bids = []
    if bids:
        return_bids.append(bids[0].serialize())
    return HttpResponse(json.dumps({'bids': return_bids}), content_type='application/json')