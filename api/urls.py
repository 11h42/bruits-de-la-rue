# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib import admin

from api import views


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^bids/$', views.handle_bids, name="handle-bids"),
    url(r'^bids/(?P<bid_id>\d+)/$', views.handle_bid, name="handle-bid"),
    url(r'^bids/(?P<bid_id>\d+)/accept/$', views.accept_bid, name="handle-bid"),
    url(r'^categories/$', views.handle_categories, name="handle-categories"),


    url(r'^users/current/$', views.get_current_user, name="user-name"),
    url(r'^users/current/address/$', views.handle_address, name="user-address"),  # todo addresses
    url(r'^users/current/associations/$', views.get_current_user_associations, name="user-association"),

    url(r'^associations/$', views.handle_associations, name="associations"),

    url(r'^faq/$', views.get_faq, name="faq"),  #todo plurialize

    url(r'^images/$', views.handle_photos, name="post_photo"),  #todo : /photos
    url(r'^images/(?P<photo_id>\d+)/$', views.handle_photo, name="post_photo"),
    url(r'^bids/status/$', views.get_status, name="status"),

    url(r'^mails/$', views.send_email, name="send_email")

    # url(r'^users/current/$', views.get_current_user, name="user-name"),
    # {'id':1234, "user_name":"gvincent"}

    # url(r'^users/(?P<user_id>\d+)/addresses/$', views.handle_user_addresses, name="user-addresses"),

    # url(r'^users/(?P<user_id>\d+)/associations/$', views.handle_associations, name="user-association"),
)