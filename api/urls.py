# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib import admin

from api import views


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^bids/$', views.handle_bids, name="handle_bids"),
    url(r'^bids/(?P<bid_id>\d+)/$', views.handle_bid, name="handle-bid"),
    url(r'^bids/(?P<bid_id>\d+)/valid/$', views.valid_bid, name="valid_bid"),
    url(r'^bids/(?P<bid_id>\d+)/accept/$', views.accept_bid, name="accept_bid"),
    url(r'^categories/$', views.handle_categories, name="categories"),
    #
    #
    url(r'^users/$', views.handle_users, name="users"),
    url(r'^users/(?P<user_id>\d+)/$', views.handle_user, name="user"),
    url(r'^addresses/$', views.handle_addresses, name="addresses"),
    url(r'^addresses/(?P<address_id>\d+)/$', views.handle_address, name='address'),
    #
    url(r'^associations/$', views.handle_associations, name="associations"),
    url(r'^associations/(?P<association_id>\d+)/$', views.handle_association, name="association"),
    url(r'^associations/(?P<association_id>\d+)/members/(?P<member_id>\d+)/$', views.handle_member, name="member"),
    #
    url(r'^faqs/$', views.handle_faqs, name="faq"),
    url(r'^faqs/(?P<faq_id>\d+)/$', views.handle_faq, name="faq"),
    #
    # url(r'^images/$', views.handle_photos, name="post_photo"),  #todo : /photos
    # url(r'^images/(?P<photo_id>\d+)/$', views.handle_photo, name="post_photo"),
    # url(r'^bids/status/$', views.get_status, name="status"),
    #
    url(r'^mails/$', views.send_email, name="send_email")
)