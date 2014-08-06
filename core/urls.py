from django.conf.urls import patterns, url

from django.contrib import admin
from core import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^login/$', views.handle_login, name='login'),
    url(r'^$', views.index, name='index'),
)