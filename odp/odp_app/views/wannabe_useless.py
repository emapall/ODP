# -*- coding: utf-8 -*-
import json
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.utils import html
from django.views.decorators.cache import cache_page
from odp_app.models import (
    Assicurazione,
    DirittoInviolabile,
    Infortunato,
    Lesione,
    Postumo,
    Professione,
    ProfiloRilevante,
    Responsabilita,
    Sentenza,
    TrendLiquidazione,
    TrendProfiloRilevante,
    TrendProfiloRilevanteContainer,
)

"""
def singup(request):
    from django.http import HttpResponseRedirect
    from lider.odp.forms import SignUpForm
    from lider.odp.tokens import account_activation_token
    from django.template.loader import render_to_string
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_domain = "www.lider-lab.sssup.it"
            subject = "Attiva il tuo Account ODP"
            message = render_to_string(
                "odp/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject, message)
            return HttpResponseRedirect(base_url + "/account_activation_sent/")
    else:
        form = SignUpForm()
    return render(request, "odp/signup.html", {"form": form})
"""

"""
def activate(request, uidb64, token):
    from django.http import HttpResponseRedirect
    from django.contrib.auth.models import User
    from django.utils.encoding import force_text
    from django.utils.http import urlsafe_base64_decode
    from lider.odp.tokens import account_activation_token

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        return HttpResponseRedirect(search_url)
    else:
        return render(request, "odp/account_activation_invalid.html")
"""
