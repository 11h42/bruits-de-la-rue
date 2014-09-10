# coding=utf-8
import json

from django.http.response import HttpResponse, HttpResponseForbidden

from api.decorators import b2rue_authenticated as is_authenticated
from api.decorators import catch_any_unexpected_exception
from api.errors import error_codes
from api.http_response import HttpMethodNotAllowed, HttpCreated, HttpBadRequest, HttpNoContent
from core.models import Bid, BidCategory, Address, User, Association, Faq, StatusBids


def get_bids(request):
    bids = Bid.objects.filter(status_bid=StatusBids.RUNNING)
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





def get_bid(request, bid_id):
    bids = Bid.objects.filter(id=bid_id)
    if bids:
        serialize = bids[0].serialize()
        serialize['current_user_id'] = request.user.id
        serialize['current_user_is_staff'] = request.user.is_staff
        return HttpResponse(json.dumps(serialize), content_type='application/json')





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
        return handle_bid_update(request, bid_id)
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


@is_authenticated
@catch_any_unexpected_exception
def get_current_user_username(request):
    return HttpResponse(request.user.username, content_type='application/json')


def create_new_address(request, user_id):
    new_address_infos = clean_dict(json.loads(request.body))
    user = User.objects.filter(id=user_id).select_related('address')
    if new_address_infos and user:
        new_address = Address(**new_address_infos)
        new_address.save()
        user[0].address.add(new_address)
        return HttpCreated()

    return HttpBadRequest(10900, error_codes['10900'])


@is_authenticated
@catch_any_unexpected_exception
def handle_address(request):
    if request.method == "GET":
        return get_current_user_address(request)
    if request.method == "POST":
        return create_new_address(request, request.user.id)
    return HttpMethodNotAllowed()


def get_current_user_address(request):
    address = Address.objects.filter(user=request.user)
    return_address = []
    if address:
        for a in address:
            return_address.append(a.serialize())
    return HttpResponse(json.dumps({'address': return_address}), content_type='application/json')


# TODO : Refactor to be under handle_associations
@is_authenticated
@catch_any_unexpected_exception
def get_current_user_associations(request):
    associations = Association.objects.filter(user=request.user)
    return_associations = []
    if associations:
        for a in associations:
            return_associations.append(a.serialize())
    return HttpResponse(json.dumps({'associations': return_associations}), content_type='application/json')


def get_associations(request):
    associations = Association.objects.all()
    return_associations = []
    if associations:
        for a in associations:
            return_associations.append(a.serialize())
    return HttpResponse(json.dumps({'associations': return_associations}), content_type='application/json')


@is_authenticated
@catch_any_unexpected_exception
def handle_associations(request):
    if request.method == "GET":
        return get_associations(request)
    return HttpMethodNotAllowed()


@is_authenticated
@catch_any_unexpected_exception
def get_faq(request):
    faqs = Faq.objects.all()
    return_faq = []
    if faqs:
        for faq in faqs:
            return_faq.append(faq.serialize())
    return HttpResponse(json.dumps({'faqs': return_faq}), content_type='application/json')


@is_authenticated
@catch_any_unexpected_exception
def get_status(request):
    return_bid_status = []
    for e in StatusBids.TYPE_CHOICES:
        return_bid_status.append({'name': str(e[0])})
    return HttpResponse(json.dumps(return_bid_status), content_type='application/json')