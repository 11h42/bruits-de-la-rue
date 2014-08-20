# -*- coding: utf-8 -*-
import re

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.template.loader import get_template
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView

from core.Forms.forms import BidForm
from core.models import Bid, User


@login_required
def index(request):
    t = get_template('index.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


def handle_login(request):
    has_error = False
    if request.method == "POST":
        has_error = True
        username = return_email_if_username(request.POST['username'])
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('core:index'))
    t = get_template('login.html')
    c = RequestContext(request, {'has_error': has_error})
    return HttpResponse(t.render(c))


def return_email_if_username(username_or_email):
    # Si le paramètre username_or_email n'est pas de la forme d'un email, on recherche si cela correspond à un username
    if not re.match(r"[^@]+@[^@]+\.[^@]+", username_or_email):
        try:
            return User.objects.get(username=username_or_email).email
        except Exception:
            return None
    else:
        # C'est un email
        return username_or_email


class BidCreate(CreateView):
    template_name = "bids/bid_form_template.html"
    form_class = BidForm

    def get_initial(self):
        initial = super(BidCreate, self).get_initial()
        initial = initial.copy()
        initial['real_author'] = self.request.user.username
        initial['end'] = ""
        initial['begin'] = ""
        initial['country'] = "France"
        return initial

    def form_valid(self, form):
        if bool(form.instance.photo) is False:
            form.instance.photo = settings.DEFAULT_BID_PHOTO
        form.instance.caller_fk_user = self.request.user
        return super(BidCreate, self).form_valid(form)


class BidUpdate(UpdateView):
    template_name = "bids/bid_form_template.html"
    form_class = BidForm
    model = Bid

    def form_valid(self, form):
        return super(BidUpdate, self).form_valid(form)


class BidDelete(DeleteView):
    model = Bid
    success_url = reverse_lazy('bid-list')


def bid_handler(request, pk):
    if request.method == "GET":
        return get_bid_details_page(request, pk)


def get_bid_details_page(request, pk):
    t = get_template('bids/detail_bid.html')
    c = RequestContext(request,
                       {"bid": get_object_or_404(Bid, pk=pk)})
    return HttpResponse(t.render(c))


class BidList(ListView):
    template_name = 'bids/list_bids.html'
    model = Bid
    context_object_name = 'bids'