# coding=utf-8
import re
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template
from core.models import User


@login_required
def index(request):
    t = get_template('index.html')
    c = RequestContext(request)
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


def display_login(request):
    has_error = False
    if request.method == "POST":
        has_error = True
        username = return_email_if_username(request.POST['username'])
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


