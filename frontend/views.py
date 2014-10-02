# coding=utf-8
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import ModelForm, widgets
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template

from frontend.forms import FrPasswordChangeForm
from core.models import Association, User


@login_required()
def index(request):
    t = get_template('index.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


def display_login(request):
    error_message = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('frontend:index'))
        else:
            error_message = "Votre mot de passe et votre login ne correspondent pas"
    t = get_template('login.html')
    c = RequestContext(request, {'error_message': error_message})
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


@staff_member_required
def display_associations(request):
    t = get_template('associations/associations.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


class AssociationForm(ModelForm):
    class Meta:
        model = Association
        fields = '__all__'
        labels = {
            'name': "Nom de l'association",
            'address': "Adresse",
            'phone': "Téléphone",
            'fax': "Fax",
            'url_site': "Site internet",
            'administrator': 'Gestionnaire'
        }
        widgets = {
            'administrator': widgets.Select(choices=User.objects.all())
        }


@staff_member_required
def add_association(request):
    if request.POST:
        association_form = AssociationForm(request.POST)
        if association_form.is_valid():
            association_form.save()
    else:
        association_form = AssociationForm()

    t = get_template('associations/add_association.html')
    c = RequestContext(request, {
        'association_form': association_form
    })

    return HttpResponse(t.render(c))


@login_required()
def display_faq(request):
    t = get_template('faq/faq.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


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


@login_required()
def create_faq(request):
    t = get_template('faq/create_faq.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


@staff_member_required
def display_association(request, association_id):
    t = get_template('associations/association.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))