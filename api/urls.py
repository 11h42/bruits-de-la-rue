# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from core import views as coreview
from api import views


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^login/$', coreview.handle_login, name='login'),
    url(r'^$', coreview.index, name='index'),

    url(r'^bids/$', views.handle_bids, name="get-bids"),
    url(r'^bids/(?P<bid_id>\d+)/$', views.handle_bid, name="get-bid"),
)