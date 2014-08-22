from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('api.urls', namespace='api')),
    url(r'^admin/', include(admin.site.urls)),
)
