# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib import admin

from api import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^bids/$', views.handle_bids, name="get-bids"),
    url(r'^bids/(?P<bid_id>\d+)/$', views.handle_bid, name="get-bid"),
)