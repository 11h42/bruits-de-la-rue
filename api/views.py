# -*- coding: utf-8 -*-
import json

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseBadRequest

from core.models.models import Bid


def handle_bids(request, bid_id):
    if request.method == "GET":
        return get_bid(request, bid_id)
    else:
        return HttpResponseBadRequest()


# TODO : Tester si bid_id est un entier ! (unicodedata.numeric ou is int ne semble pas être adaptés)

def handle_bid(request):
    if request.method == "POST":
        return post_bid(request)
    else:
        return HttpResponseBadRequest()

@login_required()
def post_bid(request):
    bid = json.loads(request.body)
    return HttpResponse()


def get_bid(request, bid_id):
    bids = Bid.objects.filter(id=bid_id)[:1]

    if bool(bids):
        bid = bids[0]
        acceptor = ""
        if bid.acceptor is not None:
            acceptor = bid.acceptor.username

        data = {u'caller': bid.caller.username,
                u'name': bid.name,
                u'acceptor': acceptor,
                u'begin': str(bid.begin),
                u'end': str(bid.end),
                u'quantity': str(bid.quantity),
                u'adress1': bid.adress1,
                u'adress2': bid.adress2,
                u'zipcode': bid.zipcode,
                u'town': bid.town,
                u'country': bid.country,
                u'real_author': bid.real_author,
                u'description': bid.description,
                u'bidCategory': bid.bidCategory.bid_category_name,
                u'photo': bid.photo.url,
                u'quantity_type': bid.quantity_type,
                u'status': bid.status,
                u'type': bid.type,
                u'emergency_level_name': bid.emergency_level.name,
                u'emergency_level_level': bid.emergency_level.level}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseBadRequest()
        # TODO : Cette fonction ne devrais pas renvoyer de réponse HTTP, mais un objet bid