from django.conf.urls import patterns, url

from frontend import views


urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.display_login, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}, name='logout'),
    url(r'^utilisateurs/nouveau/$', views.create_user, name='create_user'),
    url(r'^parametres/$', views.display_parameters, name='display_parameters'),
    url(r'^parametres/mot-de-passe/$', views.manage_password, name='manage_password'),
    url(r'^faqs/$', views.display_faqs, name='faq'),
    url(r'^faqs/creer/$', views.create_faqs, name='create_faqs'),
    url(r'^annonces/$', views.display_bids, name='bids'),
    url(r'^annonces/(?P<bid_id>\d+)/$', views.display_bid, name='display_bid'),
    url(r'^annonces/(?P<bid_id>\d+)/modifier/$', views.update_bid, name='update_bid'),
    url(r'^annonces/offre/$', views.create_bid_supply, name='create_bid_offer'),
    url(r'^annonces/demande/$', views.create_bid_demand, name='create_bid_demand'),
    url(r'^associations/$', views.display_associations, name='associations'),
    url(r'^associations/ajouter/$', views.add_association, name='add_association'),
    url(r'^associations/(?P<association_id>\d+)/$', views.display_association, name='association'),
    url(r'^associations/(?P<association_id>\d+)/editer/$', views.edit_association, name='edit_association'),
)