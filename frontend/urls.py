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

    #Annonces
    url(r'^annonces/$', views.display_bids, name='display-bids'),
    url(r'^annonces/creer$', views.create_bid, name='create-bids'),


    #Annonce
    url(r'annonces/(?P<bid_id>\d+)/$', views.display_bid, name='display-bid')
)