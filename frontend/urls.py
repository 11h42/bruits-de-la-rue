# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib import admin

from frontend import views
from frontend.views import index


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'^login/$', views.display_login, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}, name='logout'),
    url(r'^compte/motdepasse/$', views.manage_password, name="account_manage_password"),

    # Annonces
    url(r'^annonces/$', views.display_bids, name='display-bids'),
    url(r'^annonces/creer/$', views.create_bid, name='create-bids'),
    url(r'^annonces/(?P<bid_id>\d+)/$', views.display_bid, name='display-bid'),
    url(r'^annonces/(?P<bid_id>\d+)/modifier/$', views.update_bid, name='update-bid'),

    #Associations
    url(r'^associations/$', views.display_associations, name='display-association'),
    url(r'^associations/ajouter/$', views.add_association, name='add-association'),

    #FAQ
    url(r'^faq/$', views.display_faq, name='faq'),
    url(r'^faq/creer/$', views.create_faq, name='create-faq')
)