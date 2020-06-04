# -*- coding: utf-8 -*-
from django.urls import path
from django.contrib.auth import views as def_auth

from . import views as core_views

app_name = 'odp_app'

urlpatterns = [
    # path("search/s_results/", core_views.s_results,name="s-results"),    # seems not utilized anymore ^ 

    path("search_results/", core_views.new_s_results, name="search-results"),
    # path("search/i_results/", core_views.i_results), # NOT NEEDED, DONE IN NEW SEARCH
    # .....maybe?? .
    # path("search/d_results/", core_views.d_results), # NOT NEEDED, INCORPORATED IN NEW_S_RESULTS
    # infortunato and sentenza details
    path("sentenza/<int:sent_id>/<str:field_name>",core_views.get_file,name="get-file"),
    path("sentenza/<int:sent_id>", core_views.s_details,name="sentenza-details"),
    path("infortunato/<int:infort_id>/", core_views.i_details,name="infortunato-details"),
   
    path("", core_views.new_search,name="home"),
    # (r'^search/?$', 'django.views.generic.simple.direct_to_template', {'template':'odp/search.html'}) TODO TODO TODO
    # path("search/", core_views.new_search),
    # path("old_search/",core_views.old_search), #TODO LEAVE, JUST FOR DEBUG
    # path("search_ns/", core_views.search_noscript), questa c'è sul sito vero

    path("ajax/assicurazioni.json", core_views.json_assicurazioni),
    path("ajax/professioni.json", core_views.json_professioni),
    path("ajax/lesioni.json", core_views.json_lesioni),
    path("ajax/postumi.json", core_views.json_postumi),
    path("ajax/profili_rilevanti.json", core_views.json_profili_rilevanti),
    # path("ajax/profilo.json", "lider.odp.ajax.update_profilo"),
    
    path("login/", core_views.login_view,name="login"), 
    path("logout/", core_views.logout_view, name="logout"),
    # path("register/", core_views.signup), # TODO
    # path("admin/", RedirectView.as_view(url="/database/admin/")), # TODO???
    path("<schifo>/<schifo2>/",core_views.test, name="test"),
    path("signup/",core_views.signup,name="signup"),
    path("signup/confirm/<str:uid_b64>/<str:token>", core_views.signup_confirm,name="signup-confirm"),
    path("change_password/", def_auth.PasswordChangeView.as_view(), name="change-password"), # TODO: CUSTOM!
    path("reset_password/",def_auth.PasswordResetView.as_view(),name="reset-password") # TODO: CUSTOM
    

]
""" + [
    url(
        "activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/",
        core_views.activate,
        name="activate",
    )
] """
