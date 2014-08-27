# coding=utf-8
import json

from django.http.response import HttpResponse, HttpResponseNotFound

from api.decorators import b2rue_authenticated as is_authenticated
from api.decorators import catch_any_unexpected_exception
from api.http_response import HttpMethodNotAllowed
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


@is_authenticated
@catch_any_unexpected_exception
def handle_bids(request):
    if request.method == "GET":
        return get_bids(request)
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