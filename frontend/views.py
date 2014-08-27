# coding=utf-8
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template

from api.decorators import b2rue_authenticated


@b2rue_authenticated
def index(request):
    t = get_template('index.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


def display_login(request):
    has_error = False
    if request.method == "POST":
        has_error = True
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('frontend:index'))
    t = get_template('login.html')
    c = RequestContext(request, {'has_error': has_error})
    return HttpResponse(t.render(c))


def display_bids(request):
    t = get_template('bids/bids.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


def display_bid(request, bid_id):
    t = get_template('bids/bid.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))