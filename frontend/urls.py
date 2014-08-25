# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib import admin

from core import views as coreview
from frontend import views
from frontend.views import index


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'^login/$', views.display_login, name='login'),
    url(r'^annonces/$', views.display_bids, name='display-bids'),
)