# -*- coding: utf-8 -*-
from django.conf.global_settings import AUTH_USER_MODEL

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.template import RequestContext
from django.template.loader import get_template
from django.views.generic.base import TemplateView
from core.Forms.forms import OffersForm
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from core.models import Association, Bid, Message, User


@login_required
def index(request):
    t = get_template('index.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


def handle_login(request):
    has_error = False
    if request.method == "POST":
        has_error = True
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('core:index'))
    t = get_template('login.html')
    c = RequestContext(request, {'has_error': has_error})
    return HttpResponse(t.render(c))


class BidCreate(CreateView):
    model = Bid
    template_name = "offers/create_offer.html"
    fields = ['name', 'type', 'begin', 'end', 'status', 'quantity', 'localization', 'real_author', 'emergency_level',
              'recurrence', 'description', 'bidCategory']

    def form_valid(self, form):
        form.instance.caller_fk_user = User.objects.get(user=self.request.user)
        return super(BidCreate, self).form_valid(form)


class BidUpdate(UpdateView):
    model = Bid
    fields = ['name']


class BidDelete(DeleteView):
    model = Bid
    success_url = reverse_lazy('bid-list')


class BidDetails(TemplateView):
    template_name = 'offers/detail_bid.html'


class BidList(TemplateView):
    template_name = 'offers/detail_bid.html'
