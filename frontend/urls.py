# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib import admin

from core import views as coreview
from api import views


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', coreview.index, name='index'),
    url(r'^annonces/$', views.display_bids, name='display-bids'),
)