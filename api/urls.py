# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib import admin

from api import views


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^bids/$', views.handle_bids, name="handle-bids"),
    url(r'^bids/(?P<bid_id>\d+)/$', views.handle_bid, name="handle-bid"),
    url(r'^categories/$', views.handle_categories, name="handle-categories"),


    url(r'^users/current/$', views.get_current_user_username, name="current-name"),
    url(r'^users/current/address/$', views.handle_address, name="current-name"),
    url(r'^users/current/associations/$', views.handle_associations, name="current-name"),

)