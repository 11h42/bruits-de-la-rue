# coding=utf-8
import json

from django.core.mail import EmailMessage
from django.http.response import HttpResponse, HttpResponseForbidden

from api.decorators import b2rue_authenticated as is_authenticated
from api.decorators import catch_any_unexpected_exception
from api.errors import error_codes
from api.http_response import HttpMethodNotAllowed, HttpCreated, HttpBadRequest, HttpNoContent
from api.validators import BidValidator, AddressValidator
from b2rue.settings import DEFAULT_FROM_EMAIL
from core.models import Bid, BidCategory, Address, User, Association, Faq, StatusBids, Photo


def set_query_parameters(request):
    authorized_order_by = ['end', 'begin', 'title']
    order_by = request.GET.get('order_by') if request.GET.get('order_by') and request.GET.get(
        'order_by') in authorized_order_by else 'end'
    limit = request.GET.get('limit') if request.GET.get('limit') else 1000
    return limit, order_by


def get_bids(request):
    limit, order_by = set_query_parameters(request)
    bids = Bid.objects.filter(status_bid=StatusBids.RUNNING).order_by(order_by)[:limit]
    return_bids = []
    if bids:
        for bid in bids:
            return_bids.append(bid.serialize())
    return HttpResponse(json.dumps({'bids': return_bids}), content_type='application/json')


def get_bid(request, bid_id):
    bids = Bid.objects.filter(id=bid_id)
    if not bids:
        return HttpResponse({}, content_type='application/json')
    bid = bids[0].serialize()
    return HttpResponse(json.dumps({'bid': bid}), content_type='application/json')


def create_bid(request):
    json_bid = json.loads(request.body)

    bid_validator = BidValidator(json_bid)

    if not bid_validator.is_valid():
        return HttpBadRequest(bid_validator.error_code, bid_validator.error_message)

    bid = bid_validator.get_bid_object(request.user)
    new_bid = Bid(**bid)
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


def delete_bid(request, bid_id):
    bids = Bid.objects.filter(id=bid_id)
    if bids:
        bid = bids[0]
        if bid.creator == request.user or request.user.is_superuser:
            bid.delete()
            return HttpNoContent()
        return HttpResponseForbidden()
    return HttpBadRequest


def update_bid(request, bid_id):
    bids = Bid.objects.filter(id=bid_id)
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
def handle_user(request, user_id):
    if request.method == 'GET':
        return get_user(request, user_id)
    return HttpMethodNotAllowed()


def get_user(request, user_id):
    if request.GET.get('filter_by') == 'current_user':
        user = User.objects.get(id=request.user.id)
    else:
        user = User.objects.get(id=user_id)

    return HttpResponse(json.dumps({'user': user.serialize()}), content_type='application/json')


def create_address(request):
    new_address_infos = json.loads(request.body)
    user = User.objects.filter(id=request.user.id)
    address_validator = AddressValidator(new_address_infos)
    if address_validator.is_valid() and user:
        new_address = Address(**new_address_infos)
        new_address.save()
        user[0].address.add(new_address)
        return HttpCreated(json.dumps({'address': new_address.serialize()}), content_type='application/json')
    return HttpBadRequest(10900, error_codes['10900'])


@is_authenticated
@catch_any_unexpected_exception
def handle_address(request):
    if request.method == "GET":
        return get_addresses(request)
    if request.method == "POST":
        return create_address(request)
    return HttpMethodNotAllowed()


def get_addresses(request):
    address = Address.objects.filter(user=request.user)
    return_address = []
    if address:
        for a in address:
            return_address.append(a.serialize())
    return HttpResponse(json.dumps({'addresses': return_address}), content_type='application/json')


def get_associations(request):
    if request.GET.get('filter_by') == 'current_user':
        user = User.objects.get(id=request.user.id)
        associations = user.members_of.all()
    else:
        associations = Association.objects.all()
    return_associations = []
    for a in associations:
        return_associations.append(a.serialize())
    return HttpResponse(json.dumps({'associations': return_associations}), content_type='application/json')


@is_authenticated
@catch_any_unexpected_exception
def handle_associations(request):
    if request.method == "GET":
        return get_associations(request)
    return HttpMethodNotAllowed()


def create_faq(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    faq = json.loads(request.body)
    if not faq:
        return HttpBadRequest(10666, error_codes['10666'])
    new_faq = Faq(**faq)
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


def get_faqs(request):
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
        return_bid_status.append(e[0])
    return HttpResponse(json.dumps({'status': return_bid_status}), content_type='application/json')


class AcceptBidValidator():
    def __init__(self, new_bid, bid_sent, user):
        self.new_bid = new_bid
        self.bid_sent = bid_sent
        self.user = user
        self.error_code = None
        self.error_message = ''

    def is_valid(self):
        if self.new_bid.belong_to_user(self.user):
            self.error_code = 10217
            self.error_message = error_codes['10217']
        if self.new_bid.status_bid != StatusBids.RUNNING:
            self.error_code = 10220
            self.error_message = error_codes['10220']

        if 'quantity' in self.bid_sent and self.bid_sent['quantity']:
            new_quantity = self.bid_sent['quantity']
            if new_quantity < 0 or new_quantity > self.new_bid.quantity:
                self.error_code = 10218
                self.error_message = error_codes['10218']
        return len(self.error_message) == 0


@is_authenticated
@catch_any_unexpected_exception
def accept_bid(request, bid_id):
    bids = Bid.objects.filter(id=bid_id)[:1]
    bid_sent = json.loads(request.body)
    if bids and bid_sent:
        new_bid = bids[0]

        accept_bid_validator = AcceptBidValidator(new_bid, bid_sent, request.user)
        if not accept_bid_validator.is_valid():
            return HttpBadRequest(accept_bid_validator.error_code, accept_bid_validator.error_message)

        new_bid.status_bid = StatusBids.ACCEPTED
        new_bid.purchaser = request.user

        if 'quantity' in bid_sent and bid_sent['quantity']:
            new_quantity = bid_sent['quantity']
            new_bid.quantity = new_bid.quantity - new_quantity
            if new_bid.quantity != 0:
                new_bid.status_bid = StatusBids.RUNNING

        new_bid.save()
        return HttpResponse()

    return HttpBadRequest(10666, error_codes['10666'])


@is_authenticated
@catch_any_unexpected_exception
def handle_photos(request):
    if request.method == "POST":
        return post_photo(request)
    return HttpMethodNotAllowed()


def post_photo(request):
    if request.FILES is None:
        return HttpBadRequest(10221, error_codes['10221'])
    uploaded_photo = request.FILES[u'bid_image']
    photo = Photo()
    photo.owner = request.user
    photo.photo = uploaded_photo
    photo.save()
    return HttpResponse(json.dumps({'id': str(photo.pk)}), mimetype='application/json')


def get_photo(request, photo_id):
    photo = Photo.objects.filter(id=photo_id)
    if photo:
        return HttpResponse(json.dumps({'url': str(photo[0].photo.url)}), mimetype='application/json')


def delete_photo(request, photo_id):
    photos = Photo.objects.filter(id=photo_id)[:1]
    if not photos:
        return HttpBadRequest(10666, error_codes['10666'])
    if request.user != photos[0].owner and not request.user.is_superuser:
        return HttpResponseForbidden()
    bids = Bid.objects.filter(photo=photos[0])
    if bids:
        bids[0].photo = None
        bids[0].save()
    photos[0].delete()
    return HttpResponse()


@is_authenticated
@catch_any_unexpected_exception
def handle_photo(request, photo_id):
    if request.method == "GET":
        return get_photo(request, photo_id)
    if request.method == "DELETE":
        return delete_photo(request, photo_id)
    return HttpMethodNotAllowed()


@is_authenticated
@catch_any_unexpected_exception
def send_email(request):
    mail_infos = json.loads(request.body)
    if not 'user_to_mail' in mail_infos or not 'content' in mail_infos or not 'subject' in mail_infos:
        return HttpBadRequest(10666, error_codes['10666'])
    try:
        user_to = User.objects.get(username=mail_infos['user_to_mail'])
        EmailMessage(mail_infos['subject'], mail_infos['content'], DEFAULT_FROM_EMAIL,
                     [user_to.email], headers={'Reply-To': request.user.email}).send()
        if 'send_copy' in mail_infos and mail_infos['send_copy']:
            text_info_copy_mail = u"Voici une copie de l'email que vous avez envoyé à %s " \
                                  u"via l'application Bruit de la Rue : \n" % user_to.username
            EmailMessage(mail_infos['subject'], text_info_copy_mail + mail_infos['content'], DEFAULT_FROM_EMAIL,
                         [request.user.email]).send()

        return HttpResponse()
    except Exception as e:
        print e
        return HttpBadRequest(10666, error_codes['10666'])


def delete_faq(request, faq_id):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    faq = Faq.objects.filter(id=faq_id)[:1]
    if not faq:
        return HttpBadRequest(10666, error_codes['10666'])
    faq[0].delete()
    return HttpResponse()


@is_authenticated
@catch_any_unexpected_exception
def handle_faq(request, faq_id):
    if request.method == 'DELETE':
        return delete_faq(request, faq_id)
    return HttpMethodNotAllowed()


def get_association(request, association_id):
    associations = Association.objects.filter(id=association_id).select_related('members')
    if not associations:
        return HttpResponse({}, content_type='application/json')
    members = []
    for member in associations[0].members.all():
        members.append(member.serialize())
    return HttpResponse(json.dumps({'association': associations[0].serialize(), 'members': members}),
                        content_type='application/json')


def handle_association(request, association_id):
    if request.method == 'GET':
        return get_association(request, association_id)