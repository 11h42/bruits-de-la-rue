from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template

from core import models
from frontend import forms


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
            error_message = "Votre nom d'utilisateur et votre mot de passe ne correspondent pas"
    t = get_template('login.html')
    c = RequestContext(request, {'error_message': error_message})
    return HttpResponse(t.render(c))


@login_required()
def display_parameters(request):
    if request.method == 'POST':
        form = forms.UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Vos informations ont été mise à jour avec succès!")
    else:
        form = forms.UserChangeForm(instance=request.user)
    t = get_template('account/parameters.html')
    c = RequestContext(request, {'form': form})
    return HttpResponse(t.render(c))


@login_required()
def manage_password(request):
    if request.method == "POST":
        form = forms.PasswordChangeFormFR(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             "Votre mot de passe a été correctement mis à jour! Veuillez vous identifier de nouveau")
            return HttpResponseRedirect(reverse('frontend:display_parameters'))
    else:
        form = forms.PasswordChangeFormFR(user=request.user)
    t = get_template('account/manage_password.html')
    c = RequestContext(request, {
        'form': form,
    })
    return HttpResponse(t.render(c))


@login_required()
def create_bid_supply(request):
    t = get_template('bids/bid_supply.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


@login_required()
def create_bid_demand(request):
    t = get_template('bids/bid_demand.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


@login_required()
def display_faqs(request):
    t = get_template('faq/faqs.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


@login_required()
def create_faqs(request):
    t = get_template('faq/create_faq.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


@login_required()
def display_bid(request, bid_id):
    t = get_template('bids/bid.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


@login_required()
def update_bid(request, bid_id):
    bids = models.Bid.objects.filter(id=bid_id)
    if bids:
        bid_creator = bids[0].creator
        if request.user == bid_creator or request.user.is_staff:
            t = get_template('bids/bid_update.html')
            c = RequestContext(request)
            return HttpResponse(t.render(c))
    messages.add_message(request, messages.ERROR, 'Vous ne pouvez pas éditer cette annonce')
    return HttpResponseRedirect(reverse('frontend:display_bid', kwargs={'bid_id': bid_id}))


@staff_member_required
def display_associations(request):
    t = get_template('associations/associations.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


@staff_member_required
def display_association(request, association_id):
    t = get_template('associations/association.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))


@staff_member_required
def add_association(request):
    if request.method == "POST":
        form = forms.AssociationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "L'association a été ajouté avec succès")
            return HttpResponseRedirect(reverse('frontend:associations'))
    else:
        form = forms.AssociationForm()

    t = get_template('associations/add_association.html')
    c = RequestContext(request, {
        'form': form
    })

    return HttpResponse(t.render(c))


@staff_member_required
def edit_association(request, association_id):
    association = models.Association.objects.get(id=association_id)
    if request.method == "POST":
        form = forms.AssociationForm(instance=association, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "L'association %s a été mise à jour" % association.name)
            return HttpResponseRedirect(reverse('frontend:association', kwargs={'association_id': association_id}))
    else:
        form = forms.AssociationForm(instance=association)

    t = get_template('associations/add_association.html')
    c = RequestContext(request, {
        'form': form
    })

    return HttpResponse(t.render(c))


@staff_member_required
def create_user(request):
    if request.method == "POST":
        form = forms.NewUserForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "L'utilisateur a bien été créé, vous pouvez créer un nouvel utilisateur")
    else:
        form = forms.NewUserForm()

    t = get_template('associations/new_user.html')
    c = RequestContext(request, {
        'form': form
    })

    return HttpResponse(t.render(c))


@login_required()
def display_bids(request):
    t = get_template('bids/bids.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))