# -*- coding: utf-8 -*-

# from django.conf.urls.defaults import *
from django.urls import path
from odp_app import views as core_views

urlpatterns = [
    path("search/s_results/", core_views.s_results),
    path("search/new_s_results/", core_views.new_s_results),
    path("search/s_details/", core_views.s_details),
    path("search/i_results/", core_views.i_results),
    path("search/i_details/", core_views.i_details),
    path("search/d_results/", core_views.d_results),
    # (r'^search/?$', 'django.views.generic.simple.direct_to_template', {'template':'odp/search.html'}),
    path("search/", core_views.new_search),
    path("/", core_views.new_search),
    # path("search_ns/", core_views.search_noscript),
    path("ajax/assicurazioni.json", core_views.json_assicurazioni),
    path("ajax/professioni.json", core_views.json_professioni),
    path("ajax/lesioni.json", core_views.json_lesioni),
    path("ajax/postumi.json", core_views.json_postumi),
    path("ajax/profili_rilevanti.json", core_views.json_profili_rilevanti),
    # path("ajax/profilo.json", "lider.odp.ajax.update_profilo"),
    # path("login/", "django.contrib.auth.views.login", {"template_name": "odp/login.html"}), # TODO
    path("logout/", core_views.logout_view),
    # path("register/", core_views.singup), # TODO
    # path("admin/", RedirectView.as_view(url="/database/admin/")), # TODO
    path("account_activation_sent/", core_views.account_activation_sent),
]
""" + [
    url(
        "activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/",
        core_views.activate,
        name="activate",
    )
] """
