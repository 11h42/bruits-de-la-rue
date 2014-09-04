# coding=utf-8
import json

from django.http.response import HttpResponse, HttpResponseForbidden

from api.decorators import b2rue_authenticated as is_authenticated
from api.decorators import catch_any_unexpected_exception
from api.errors import error_codes
from api.http_response import HttpMethodNotAllowed, HttpCreated, HttpBadRequest, HttpNoContent
from api.validators import BidValidator
from core.models import Bid, BidCategory


def get_bids(request):
    bids = Bid.objects.filter(status="RUNNING")
    return_bids = []
    if bids:
        for bid in bids:
            return_bids.append(bid.serialize())
    return HttpResponse(json.dumps({'bids': return_bids}), content_type='application/json')


def clean_dict(dict):
    """
    :param dict: 
    :return: The dict containing only fields with values.
    """
    cleaned_dict = {}
    for key, value in dict.items():
        if value:
            cleaned_dict[key] = value
    return cleaned_dict


def create_bid(request):
    bid_cleaned = clean_dict(json.loads(request.body))
    if bid_cleaned:
        bid_validator = BidValidator()
        if bid_validator.bid_is_valid(bid_cleaned):
            bid_cleaned['creator'] = request.user
            if 'category' in bid_cleaned:
                bid_cleaned['category'], created = BidCategory.objects.get_or_create(
                    name=bid_cleaned['category']['name'])
        if 'begin' in bid_cleaned and 'end' in bid_cleaned:
            if bid_cleaned['begin'] > bid_cleaned['end']:
                return HttpBadRequest(10215, error_codes['10215'])
        new_bid = Bid(**bid_cleaned)
        new_bid.save()
        new_bid_id = new_bid.id
        return HttpCreated(json.dumps({'bid_id': new_bid_id}), location='/api/bids/%d/' % new_bid_id)
    return HttpBadRequest(10900, error_codes['10900'])


def get_bid(request, bid_id):
    bids = Bid.objects.filter(id=bid_id)
    if bids:
        serialize = bids[0].serialize()
        serialize['current_user_id'] = request.user.id
        serialize['current_user_is_staff'] = request.user.is_staff
        return HttpResponse(json.dumps(serialize), content_type='application/json')


def accept_bid(request, bid_dict, matching_bid):
    user = request.user
    if user != matching_bid.creator and matching_bid.status == "RUNNING":
        matching_bid_serialized = matching_bid.serialize()
        for key, value in bid_dict.items():
            if key != 'status' and key != 'purchaser':
                if value != matching_bid_serialized[key]:
                    return HttpBadRequest(10900, error_codes['10900'])
        matching_bid.purchaser = user
        matching_bid.status = "ACCEPTED"
        matching_bid.save()
        return HttpResponse()
    return HttpBadRequest(10217, error_codes['10217'])


def update_bid(request, bid_id):
    bid_dict = clean_dict(json.loads(request.body))
    matching_bid = Bid.objects.filter(id=bid_dict['id'])
    bid_validator = BidValidator()
    if matching_bid and bid_dict:
        bid_dict.pop('creator', None)
        bid_dict.pop('current_user_is_staff', None)
        bid_dict.pop('current_user_id', None)
        bid = matching_bid[0]
        if 'status' in bid_dict and bid_dict['status'] == 'ACCEPTED':
            return accept_bid(request, bid_dict, bid)
        if bid.creator == request.user or request.user.is_staff:
            if bid_validator.bid_is_valid(bid_dict):
                matching_bid.update(**bid_dict)
                return HttpResponse()
        return HttpBadRequest(10216, error_codes['10216'])
    return HttpBadRequest(10900, error_codes['10900'])


@is_authenticated
@catch_any_unexpected_exception
def handle_bids(request):
    if request.method == "GET":
        return get_bids(request)

    if request.method == "POST":
        return create_bid(request)
    return HttpMethodNotAllowed()


def delete_bid(request, bid_id):
    bids = Bid.objects.filter(id=bid_id)
    if bids:
        bid = bids[0]
        if bid.creator == request.user or request.user.is_staff:
            bid.delete()
            return HttpNoContent()
        return HttpResponseForbidden()
    return HttpBadRequest


@is_authenticated
@catch_any_unexpected_exception
def handle_bid(request, bid_id):
    if request.method == 'GET':
        return get_bid(request, bid_id)
    if request.method == 'PUT':
        return update_bid(request, bid_id)
    if request.method == 'DELETE':
        return delete_bid(request, bid_id)
    return HttpMethodNotAllowed()


def get_available_categories(request):
    categories = BidCategory.objects.all()
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