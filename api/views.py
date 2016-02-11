import json
import logging

from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound
from api.decorators import catch_any_unexpected_exception
from api.decorators import b2rue_authenticated as is_authenticated
from api.errors import error_codes
from api.http_response import HttpMethodNotAllowed, HttpCreated, HttpBadRequest, HttpNoContent, HttpResponseUnauthorized
from api.validators import BidValidator, AddressValidator
from b2rue.settings import DEFAULT_FROM_EMAIL
from core import models


logger = logging.getLogger(__name__)


def set_query_parameters(request):
    authorized_order_by = ['end', 'begin', 'title']
    order_by = '-end'
    if request.GET.get('order_by') and request.GET.get('order_by') in authorized_order_by:
        order_by = request.GET.get('order_by')
    limit = int(request.GET.get('limit')) if request.GET.get('limit') else 1000
    return limit, order_by


def get_bids(request):
    limit, order_by = set_query_parameters(request)
    user = request.user
    bids = models.Bid.objects.filter(Q(creator=user) | Q(purchaser=user) | Q(status_bid=models.StatusBids.RUNNING))
    bids = bids.order_by(order_by)[:limit]
    return_bids = []
    if bids:
        for bid in bids:
            return_bids.append(bid.serialize())
    return HttpResponse(json.dumps({'bids': return_bids}), content_type='application/json')


def create_bid(request):
    json_bid = json.loads(request.body.decode('utf-8'))
    bid_validator = BidValidator(json_bid)
    if not bid_validator.is_valid():
        logger.debug('bid is not valid : %s' % bid_validator.error_message)
        return HttpBadRequest(bid_validator.error_code, bid_validator.error_message)

    bid = bid_validator.get_bid_object(request.user)
    new_bid = models.Bid(**bid)
    new_bid.save()
    new_bid_id = new_bid.id
    return HttpCreated(json.dumps({'bid_id': new_bid_id}), location='/api/bids/%d/' % new_bid_id)


@is_authenticated
@catch_any_unexpected_exception
def handle_bids(request):
    if request.method == "GET":
        return get_bids(request)
    if request.method == "POST":
        return create_bid(request)
    return HttpMethodNotAllowed()


def create_address(request):
    new_address_infos = json.loads(request.body.decode('utf-8'))
    address_validator = AddressValidator(new_address_infos)
    user = request.user
    if address_validator.is_valid() and user:
        new_address = models.Address(**new_address_infos)
        new_address.save()
        user.addresses.add(new_address)
        location = reverse('api:address', kwargs={'address_id': new_address.id})
        return HttpCreated(location=location)
    return HttpBadRequest(10900, error_codes['10900'])


def get_addresses(request):
    addresses = models.Address.objects.filter(user=request.user)
    return_addresses = []
    if addresses:
        for address in addresses:
            return_addresses.append(address.serialize())
    return HttpResponse(json.dumps({'addresses': return_addresses}), content_type='application/json')


@is_authenticated
@catch_any_unexpected_exception
def handle_addresses(request):
    if request.method == "GET":
        return get_addresses(request)
    if request.method == "POST":
        return create_address(request)
    return HttpMethodNotAllowed()


def get_address(request, address_id):
    addresses = models.Address.objects.filter(id=address_id, user=request.user)[:1]
    if addresses:
        return HttpResponse(json.dumps(addresses[0].serialize()), content_type='application/json')
    return HttpResponseNotFound()


@is_authenticated
@catch_any_unexpected_exception
def handle_address(request, address_id):
    if request.method == "GET":
        return get_address(request, address_id)
    return HttpMethodNotAllowed()


def get_categories(request):
    categories = models.BidCategory.objects.all()
    returned_categories = []
    if categories:
        for category in categories:
            returned_categories.append(category.serialize())
    return HttpResponse(json.dumps({'categories': returned_categories}), content_type='application/json')


@is_authenticated
@catch_any_unexpected_exception
def handle_categories(request):
    if request.method == "GET":
        return get_categories(request)
    return HttpMethodNotAllowed()


def get_associations(request):
    associations = models.Association.objects.all()
    return_associations = []
    for association in associations:
        return_associations.append(association.serialize())
    return HttpResponse(json.dumps({'associations': return_associations}), content_type='application/json')


@is_authenticated
@catch_any_unexpected_exception
def handle_associations(request):
    if request.method == "GET":
        return get_associations(request)
    return HttpMethodNotAllowed()


def get_faqs(request):
    faqs = models.Faq.objects.all()
    return_faq = []
    if faqs:
        for faq in faqs:
            return_faq.append(faq.serialize())
    return HttpResponse(json.dumps({'faqs': return_faq}), content_type='application/json')


def create_faq(request):
    faq = json.loads(request.body.decode('utf-8'))
    if not faq:
        return HttpBadRequest(10666, error_codes['10666'])
    new_faq = models.Faq(**faq)
    new_faq.save()
    return HttpCreated()


@is_authenticated
@catch_any_unexpected_exception
def handle_faqs(request):
    if request.method == 'POST':
        return create_faq(request)
    if request.method == 'GET':
        return get_faqs(request)
    return HttpMethodNotAllowed()


def delete_faq(request, faq_id):
    faqs = models.Faq.objects.filter(id=faq_id)[:1]
    if faqs and request.user.is_staff:
        faqs[0].delete()
        return HttpNoContent()
    return HttpBadRequest(10666, error_codes['10666'])


@is_authenticated
@catch_any_unexpected_exception
def handle_faq(request, faq_id):
    if request.method == 'DELETE':
        return delete_faq(request, faq_id)
    return HttpMethodNotAllowed()


def get_bid(request, bid_id):
    bids = models.Bid.objects.filter(id=bid_id)
    if not bids:
        return HttpResponse({}, content_type='application/json')
    bid = bids[0].serialize()
    return HttpResponse(json.dumps({'bid': bid}), content_type='application/json')


def delete_bid(request, bid_id):
    bids = models.Bid.objects.filter(id=bid_id)
    if bids:
        bid = bids[0]
        if bid.creator == request.user or request.user.is_staff:
            bid.delete()
            return HttpNoContent()
    return HttpBadRequest(10666, error_codes['10666'])


def update_bid(request, bid_id):
    bids = models.Bid.objects.filter(id=bid_id)
    new_bid = json.loads(request.body)
    if bids and new_bid:
        bid_creator = bids[0].creator
        bid_validator = BidValidator(new_bid)
        if request.user == bid_creator or request.user.is_staff:
            if bid_validator.is_valid():
                updated_bid = bid_validator.get_bid_object(bid_creator)
                bids.update(**updated_bid)
                return HttpResponse(json.dumps({'bid_id': bids[0].id}), content_type='application/json')
        return HttpBadRequest(10666, bid_validator.error_message)

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


@is_authenticated
@catch_any_unexpected_exception
def send_email(request):
    mail_infos = json.loads(request.body.decode('utf-8'))
    if 'user_to_mail' not in mail_infos or 'content' not in mail_infos or 'subject' not in mail_infos:
        return HttpBadRequest(10666, error_codes['10666'])
    user_to = models.User.objects.get(username=mail_infos['user_to_mail'])
    email = EmailMessage(mail_infos['subject'], mail_infos['content'], DEFAULT_FROM_EMAIL, [user_to.email],
                         headers={'Reply-To': request.user.email})
    email.send()
    return HttpCreated()


@is_authenticated
@catch_any_unexpected_exception
def accept_bid(request, bid_id):
    bids = models.Bid.objects.filter(id=bid_id)[:1]
    bid_sent = json.loads(request.body.decode('utf-8'))

    if bids and bid_sent:
        new_bid = bids[0]
        new_bid.status_bid = models.StatusBids.ACCEPTED
        new_bid.purchaser = request.user

        if 'desired_amount' in bid_sent and bid_sent['desired_amount']:
            new_bid.quantity = new_bid.quantity - bid_sent['desired_amount']
            if new_bid.quantity != 0:
                new_bid.status_bid = models.StatusBids.RUNNING
        new_bid.save()
        return HttpResponse()
    return HttpBadRequest(10666, error_codes['10666'])


def get_association(request, association_id):
    association = models.Association.objects.filter(id=association_id).first()
    if association:
        return HttpResponse(json.dumps({'association': association.serialize(True)}), content_type='application/json')
    return HttpBadRequest(10666, error_codes['10666'])


def delete_association(request, association_id):
    associations = models.Association.objects.filter(id=association_id)[:1]
    if associations and request.user.is_superuser:
        associations[0].delete()
        return HttpNoContent()
    return HttpBadRequest(10666, error_codes['10666'])


@is_authenticated
@catch_any_unexpected_exception
def handle_association(request, association_id):
    if request.method == 'GET':
        return get_association(request, association_id)
    if request.method == 'DELETE':
        return delete_association(request, association_id)
    return HttpMethodNotAllowed()


def delete_member_in_association(request, association_id, member_id):
    associations = models.Association.objects.filter(id=association_id)[:1]
    members = models.User.objects.filter(id=member_id)[:1]
    if associations and members and request.user.is_staff:
        associations[0].members.remove(members[0])
        return HttpNoContent()
    return HttpBadRequest(10666, error_codes['10666'])


def add_member_in_association(request, association_id, member_id):
    associations = models.Association.objects.filter(id=association_id)[:1]
    members = models.User.objects.filter(id=member_id)[:1]
    if associations and members and request.user.is_staff:
        members[0].associations.add(associations[0])
        return HttpCreated()
    return HttpBadRequest(10666, error_codes['10666'])


@is_authenticated
@catch_any_unexpected_exception
def handle_member(request, association_id, member_id):
    if request.method == 'POST':
        return add_member_in_association(request, association_id, member_id)
    if request.method == 'DELETE':
        return delete_member_in_association(request, association_id, member_id)
    return HttpMethodNotAllowed()


def get_users(request):
    if request.user.is_staff:
        users = models.User.objects.all().exclude(is_superuser=True)
        return_users = []
        for user in users:
            return_users.append(user.serialize())
        return HttpResponse(json.dumps({'users': return_users}), content_type='application/json')
    return HttpResponseUnauthorized()


@is_authenticated
@catch_any_unexpected_exception
def handle_users(request):
    if request.method == 'GET':
        return get_users(request)
    return HttpMethodNotAllowed()


def delete_user(request, user_id):
    if request.user.is_staff:
        users = models.User.objects.filter(id=user_id)[:1]
        if users:
            users[0].delete()
            return HttpNoContent()
        return HttpResponseNotFound()
    return HttpResponseUnauthorized()


@is_authenticated
@catch_any_unexpected_exception
def handle_user(request, user_id):
    if request.method == 'DELETE':
        return delete_user(request, user_id)
    return HttpMethodNotAllowed()

