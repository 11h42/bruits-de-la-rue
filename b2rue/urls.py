from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^api/', include('api.urls', namespace='api')),

    url(r'^', include('frontend.urls', namespace='frontend')),

    url(r'^admin/', include(admin.site.urls)),
)
