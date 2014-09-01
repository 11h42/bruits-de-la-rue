# coding=utf-8
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template


@login_required()
def index(request):
    t = get_template('index.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


def display_login(request):
    if hasattr(request, "user") and request.user.is_authenticated():
        return HttpResponseRedirect(reverse('frontend:index'))
    else:
        has_error = False
        # todo : Test if the user is already logged on. If true, redirect to index with warning message
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


@login_required()
def display_bids(request):
    t = get_template('bids/bids.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


@login_required()
def display_bid(request, bid_id):
    t = get_template('bids/bid.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


@login_required()
def create_bid(request):
    t = get_template('bids/create_bid.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))