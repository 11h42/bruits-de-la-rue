from django.conf.urls import patterns, include, url

from django.contrib import admin
from b2rue import settings

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^api/', include('api.urls', namespace='api')),

    url(r'^', include('frontend.urls', namespace='frontend')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    url(r'^admin/', include(admin.site.urls)),
)