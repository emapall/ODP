# -*- coding: utf-8 -*-

#from django.conf.urls.defaults import *
from django.conf.urls import *
from django.views.generic import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from lider.odp import views as core_views

urlpatterns = patterns('',

	(r'^search/s_results/$', 'lider.odp.views.s_results'),
	(r'^search/new_s_results/$', 'lider.odp.views.new_s_results'),
	(r'^search/s_details/$', 'lider.odp.views.s_details'),

	(r'^search/i_results/$', 'lider.odp.views.i_results'),
	(r'^search/i_details/$', 'lider.odp.views.i_details'),

	(r'^search/d_results/$', 'lider.odp.views.d_results'),

#	(r'^search/?$', 'django.views.generic.simple.direct_to_template', {'template':'odp/search.html'}),
	(r'^search/?$', 'lider.odp.views.new_search'),
	(r'^/?$', 'lider.odp.views.new_search'),
	(r'^search_ns/?$', 'lider.odp.views.search_noscript'),

	(r'^ajax/assicurazioni.json$', 'lider.odp.views.json_assicurazioni'),
	(r'^ajax/professioni.json$', 'lider.odp.views.json_professioni'),
	(r'^ajax/lesioni.json$', 'lider.odp.views.json_lesioni'),
	(r'^ajax/postumi.json$', 'lider.odp.views.json_postumi'),
	(r'^ajax/profili_rilevanti.json$', 'lider.odp.views.json_profili_rilevanti'),

	(r'^ajax/profilo.json$', 'lider.odp.ajax.update_profilo'),
	
	(r'^login/?$', 'django.contrib.auth.views.login', {'template_name': 'odp/login.html'}),
	(r'^logout/?$', 'lider.odp.views.logout_view'),

	(r'^register/?$', 'lider.odp.views.singup'),

	(r'^admin/?', RedirectView.as_view(url='/database/admin/')),

	(r'^new_search/?$', 'lider.odp.views.new_search'),
	(r'^account_activation_sent/$', 'lider.odp.views.account_activation_sent'),
) + [url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', core_views.activate, name='activate'),]
