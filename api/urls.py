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
    url(r'^annonce/(?P<bid_id>\d+)/$', views.handle_bid, name="get-bid"),
    url(r'^annonce/liste/$', coreview.BidList.as_view(), name="get-list-bid"),
    url(r'^annonce/creer/$', coreview.BidCreate.as_view(), name='post-bid'),
    url(r'^annonce/(?P<pk>[0-9]+)/update/$', coreview.BidUpdate.as_view(), name='update-bid'),
    url(r'^annonce/(?P<pk>[0-9]+)/delete/$', coreview.BidDelete.as_view(), name='delete-bid'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# TODO: + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) Cette ligne sert en gros uniquement au DEBUG, inutilisable en prod, il faut la remplacer en utilisant le système de gestion de fichiers statiques ?