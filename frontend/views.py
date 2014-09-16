# coding=utf-8
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from django.template.loader import get_template

from frontend.forms import FrPasswordChangeForm


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


@login_required()
def update_bid(request, bid_id):
    t = get_template('bids/update_bid.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


@login_required()
def display_associations(request):
    t = get_template('associations/associations.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


@login_required()
def display_faq(request):
    t = get_template('faq/faq.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


@login_required()
def manage_password_done(request):
    messages.success(request, 'Votre mot de passe à bien été mis à jour')
    return HttpResponseRedirect(reverse("frontend:account_manage_password"))


@login_required()
def manage_password(request):
    password_changed = False
    if request.method == "POST":
        form = FrPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            password_changed = True
    else:
        form = FrPasswordChangeForm(user=request.user)
    t = get_template('users/manage_password.html')
    c = RequestContext(request, {
        'form': form,
        'password_changed': password_changed
    })
    return HttpResponse(t.render(c))


def create_faq(request):
    t = get_template('faq/create_faq.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))