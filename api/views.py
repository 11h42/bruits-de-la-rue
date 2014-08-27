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















        # # TODO : Tester si bid_id est un entier ! (unicodedata.numeric ou is int ne semble pas être adaptés)
        #
        # def handle_bid(request):
        # if request.method == "POST":
        # return post_bid(request)
        # else:
        # return HttpResponseBadRequest()
        #
        #
        # @is_authenticated()
        # def post_bid(request):
        # bid = json.loads(request.body)
        # data = {
        # u'caller': Bid.objects.get(bid.user.id),
        # u'name': bid.name,
        # u'acceptor': bid.acceptor,
        # u'begin': time.strptime(bid.begin,"%d%b%Y"),
        # u'end': time.strptime(bid.begin,"%d%b%Y")str(bid.end),
        # u'quantity': str(bid.quantity),
        # u'adress1': bid.adress1,
        # u'adress2': bid.adress2,
        # u'zipcode': bid.zipcode,
        # u'town': bid.town,
        # u'country': bid.country,
        # u'real_author': bid.real_author,
        # u'description': bid.description,
        #             u'bidCategory': bid.bidCategory.bid_category_name,
        #             u'photo': bid.photo.url,
        #             u'quantity_type': bid.quantity_type,
        #             u'status': bid.status,
        #             u'type': bid.type,
        #             u'emergency_level_name': bid.emergency_level.name,
        #             u'emergency_level_level': bid.emergency_level.level
        #         }
        #     new_bid = Bid(**bid)
        #     new_bid.save()
        #     try:
        #         print("toto")
        #     except Exception:
        #         print("Tu m'tonne")
        #     return HttpResponse()
        #
        #
        # # TODO : Ce truc. En gros comment check que tous les éléments sont présents et biens formattés, avec le moins de code possible .. sans se répéter. Pour le moment aucune idée.
        #
        #
        # def get_bid(request, bid_id):
        #     bids = Bid.objects.filter(id=bid_id)[:1]
        #
        #     if bool(bids):
        #         bid = bids[0]
        #         acceptor = ""
        #         if bid.acceptor is not None:
        #             acceptor = bid.acceptor.username
        #
        #         data = {
        #             u'caller': bid.caller.username,
        #             u'name': bid.name,
        #             u'acceptor': acceptor,
        #             u'begin': str(bid.begin),
        #             u'end': str(bid.end),
        #             u'quantity': str(bid.quantity),
        #             u'adress1': bid.adress1,
        #             u'adress2': bid.adress2,
        #             u'zipcode': bid.zipcode,
        #             u'town': bid.town,
        #             u'country': bid.country,
        #             u'real_author': bid.real_author,
        #             u'description': bid.description,
        #             u'bidCategory': bid.bidCategory.bid_category_name,
        #             u'photo': bid.photo.url,
        #             u'quantity_type': bid.quantity_type,
        #             u'status': bid.status,
        #             u'type': bid.type,
        #             u'emergency_level_name': bid.emergency_level.name,
        #             u'emergency_level_level': bid.emergency_level.level
        #         }
        #         return HttpResponse(json.dumps(data), content_type='application/json')
        #     else:
        #         return HttpResponseBadRequest()
        #         # TODO : Cette fonction ne devrais pas renvoyer de réponse HTTP, mais un objet bid