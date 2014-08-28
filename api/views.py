# coding=utf-8
import json

from django.http.response import HttpResponse, HttpResponseBadRequest

from api import validators

from api.decorators import b2rue_authenticated as is_authenticated
from api.decorators import catch_any_unexpected_exception
from api.http_response import HttpMethodNotAllowed, HttpCreated
from core.models import Bid, User


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
        if validators.json_bid_is_valid(bid) is True:
            new_bid = Bid()
            new_bid.creator = User.objects.filter(id=bid['creator'])[0]
            new_bid.title = bid['title']
            new_bid.description = bid['description']
            new_bid.save()
            return HttpCreated(json.dumps({'bid_id': new_bid.id}))
    return HttpResponseBadRequest()


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