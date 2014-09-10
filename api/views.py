# coding=utf-8
import json

from django.http.response import HttpResponse, HttpResponseForbidden

from api import constants
from api.decorators import b2rue_authenticated as is_authenticated
from api.decorators import catch_any_unexpected_exception
from api.errors import error_codes
from api.http_response import HttpMethodNotAllowed, HttpCreated, HttpBadRequest, HttpNoContent
from api.validators import BidValidator
from core.models import Bid, BidCategory, Address, User, Association, Faq, StatusBids


def get_bids(request):
    bids = Bid.objects.filter(status_bid=StatusBids.RUNNING)
    return_bids = []
    if bids:
        for bid in bids:
            return_bids.append(bid.serialize())
    return HttpResponse(json.dumps({'bids': return_bids}), content_type='application/json')


def clean_dict(dict):
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


def set_bid_objects_fields(bid_sent):
    if 'category' in bid_sent:
        bid_sent['category'] = BidCategory.objects.get(id=bid_sent['category']['id'])
    if 'localization' in bid_sent:
        bid_sent['localization'] = Address.objects.get(id=bid_sent['localization']['id'])
    if 'association' in bid_sent:
        bid_sent['association'] = Association.objects.get(id=bid_sent['association']['id'])


def create_bid(request):
    bid_sent = clean_dict(json.loads(request.body))
    bid_validator = BidValidator()
    bid_errors = bid_validator.bid_is_valid(bid_sent)
    if bid_sent:
        if len(bid_errors) == 0:
            bid_sent['creator'] = request.user
            if 'begin' in bid_sent and bid_sent['begin'] > constants.TODAY_ISO:
                bid_sent['status_bid'] = StatusBids.ONHOLD
            set_bid_objects_fields(bid_sent)
            new_bid = Bid(**bid_sent)
            new_bid.save()
            new_bid_id = new_bid.id
            return HttpCreated(json.dumps({'bid_id': new_bid_id}), location='/api/bids/%d/' % new_bid_id)
        else:
            return HttpBadRequest(10666, bid_errors)


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


def update_bid(request, bid_id):
    bid = Bid.objects.filter(id=bid_id)
    bid_sent = clean_dict(json.loads(request.body))
    if bid and bid_sent:
        if request.user == bid[0].creator or request.user.is_staff:
            bid_validator = BidValidator()
            if len(bid_validator.bid_is_valid(bid_sent)) == 0:
                bid.update(**bid_sent)
                return HttpResponse()
        return HttpBadRequest(10216, error_codes['10216'])
    return HttpBadRequest(10666, error_codes['10666'])


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


@is_authenticated
@catch_any_unexpected_exception
def accept_bid(request, bid_id):
    bid = Bid.objects.filter(id=bid_id)
    bid_sent = clean_dict(json.loads(request.body))
    if bid and bid_sent:
        bid_to_update = bid[0]
        if request.user != bid_to_update.creator:
            if bid_to_update.status_bid == StatusBids.RUNNING:
                if 'quantity' in bid_sent:
                    if 0 < bid_sent['quantity'] <= bid_to_update.quantity:
                        bid_to_update.quantity = bid_to_update.quantity - bid_sent['quantity']
                        bid_to_update.purchaser = request.user
                        if bid_to_update.quantity == 0:
                            bid_to_update.status_bid = StatusBids.ACCEPTED
                    else:
                        return HttpBadRequest(10218, error_codes['10218'])

                else:
                    bid_to_update.status_bid = StatusBids.ACCEPTED
                    bid_to_update.purchaser = request.user
                bid_to_update.save()
                return HttpResponse()
            else:
                return HttpBadRequest(10220, error_codes['10220'])
        else:
            return HttpBadRequest(10217, error_codes['10217'])
    return HttpBadRequest(10666, error_codes['10666'])