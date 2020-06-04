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

def old_search(request):
    return render(request, "odp/search.html", {})

"""
def signup(request):
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


"""
I results viene chiamata solo nella search vecchia, + sembra assai scarna coi filtri.
Inoltre sul sito vero non viene chiamata(mai?)
"""
def i_results(request):
    from django.core.exceptions import ValidationError

    obj = Infortunato.objects.all()

    try:
        if request.GET.get("eta"):
            obj = obj.filter(eta=request.GET["eta"])
        if "est_maggiorenne" in request.GET:
            obj = obj.filter(est_maggiorenne=request.GET["est_maggiorenne"])
            if request.GET["est_maggiorenne"] == 0:
                obj = obj.filter(eta__lte=18)

        if request.GET.get("sesso"):
            obj = obj.filter(sesso=request.GET["sesso"])
        if request.GET.get("professione"):
            obj = obj.filter(professione=request.GET["professione"])
        if request.GET.get("lesione"):
            nobj = obj.filter(id=(-1))
            for unalesione in request.GET.getlist("lesione"):
                nobj = nobj | obj.filter(lesione=unalesione)
            obj = nobj
        if request.GET.get("postumo"):
            nobj = obj.filter(id=(-1))
            for unpostumo in request.GET.getlist("postumo"):
                nobj = nobj | obj.filter(postumo=unpostumo)
            obj = nobj
        if "ante_2001" not in request.GET:
            obj = obj.filter(pre2001=False)
        if not request.user.is_staff:
            obj = obj.filter(pubblicabile=True)

    except ValidationError as e:
        mess = (
            "Hai inserito una ricerca non valida:<br/><strong>"
            + "<br/>".join(map(html.escape, e.messages))
            + "</strong>"
        )
        return render(request, "errore.html", {"mess": mess})

    else:
        return do_paging_response(request, obj, "odp/i_results.html")


i_results = check_auth(i_results)

# --------------- SENTENZA RESULTS ------ PUÒ ESSERE UTILE

def d_results(request):
    from django.core.exceptions import ValidationError

    obj = Infortunato.objects.all()

    try:
        if request.GET.get("perc_ip_da"):
            obj = obj.filter(percentuale_das_ip__gte=request.GET["perc_ip_da"])
        if request.GET.get("perc_ip_a"):
            obj = obj.filter(percentuale_das_ip__lte=request.GET["perc_ip_a"])
        if request.GET.get("metodo_das_ip"):
            obj = obj.filter(metodo_das_ip=request.GET["metodo_das_ip"])

        if "sede_tabella" in request.GET:
            obj = obj.filter(sede_tabella=request.GET["sede_tabella"])

        if "est_clg" in request.GET:
            obj = obj.filter(est_clg=True)
        if "est_cls" in request.GET:
            obj = obj.filter(est_cls=True)

        if "est_lcip" in request.GET:
            obj = obj.filter(est_lcip=True)

        if "est_it" in request.GET:
            obj = obj.filter(est_it=True)
        if request.GET.get("metodo_das_it"):
            obj = obj.filter(metodo_das_it=request.GET["metodo_das_it"])

        if "est_lcit" in request.GET:
            obj = obj.filter(est_lcit=True)

        if "est_dm" in request.GET:
            obj = obj.filter(est_dm=True)
        if "metodo_dm" in request.GET:
            metodo = request.GET["metodo_dm"]
            if metodo == "equi":
                obj = obj.filter(est_dm_vp=True)
            elif metodo == "perma":
                obj = obj.filter(est_dm_ip=True)
            elif metodo == "temp":
                obj = obj.filter(est_dm_it=True)

        if "danno_np" in request.GET:
            obj = obj.filter(sunt_diritti_lesi=True)
        if "diritti_lesi" in request.GET:
            diritto = request.GET["diritti_lesi"]
            if diritto != "":
                obj = obj.filter(dirittoinviolabile__id=diritto)

        if "danno_morte" in request.GET:
            obj = obj.filter(dm_est=True)

        if "danno_p" in request.GET:
            danno = request.GET["danno_p"]
            if danno == "spese_sostenute":
                obj = obj.filter(est_ss=True)
            elif metodo == "spese_future":
                obj = obj.filter(est_ss_future=True)
            # TODO altri danni come fare??

        if "trend_liq" in request.GET:
            trend = request.GET["trend_liq"]
            if trend != "":
                obj = obj.filter(trend_liquidazione__id=trend)

        if "ante_2001" not in request.GET:
            obj = obj.filter(pre2001=False)

    except ValidationError as e:
        mess = (
            "Hai inserito una ricerca non valida:<br/><strong>"
            + "<br/>".join(map(html.escape, e.messages))
            + "</strong>"
        )
        return render(request, "errore.html", {"mess": mess})

    else:
        return do_paging_response(request, obj, "odp/i_results.html")

d_results = check_auth(d_results)


###### /search: ricerca ########################


def search(request):
    responsabilita = Responsabilita.objects.all()
    diritti_lesi = DirittoInviolabile.objects.all()
    trend_liq = TrendLiquidazione.objects.all()
    parole_chiave = TrendProfiloRilevante.objects.all()
    return render(
        request,
        "odp/search.html",
        {
            "responsabilita": responsabilita,
            "diritti_lesi": diritti_lesi,
            "trend_liq": trend_liq,
            "parole_chiave": parole_chiave,
        },
    )

search = check_auth(search)

