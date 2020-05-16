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

def s_results(request):
    """
        Praticamente è uguale a new_s_results, ma 
        - manca tutta la parte di filtraggio sugli infortunati
        - ci sono cose aggiuntive come parole_chiave, ante_2001, profili rilevanti
        - praticamente tutta sta roba è stata sostituita da contesto testuale e basta (ma è giusto?)
    """
    from django.core.exceptions import ValidationError

    obj = Sentenza.objects.all()

    try:
        if request.GET.get("grado_di_giudizio"):
            obj = obj.filter(grado_di_giudizio__contains=request.GET["grado_di_giudizio"])
        if request.GET.get("data_della_sentenza"):
            obj = obj.filter(data_della_sentenza=request.GET["data_della_sentenza"])
        if request.GET.get("data_del_deposito"):
            obj = obj.filter(data_del_deposito=request.GET["data_del_deposito"])
        if request.GET.get("numero_della_sentenza"):
            obj = obj.filter(numero_della_sentenza=request.GET["numero_della_sentenza"])
        if request.GET.get("estensore"):
            obj = obj.filter(estensore__contains=request.GET["estensore"])
        if request.GET.get("anno_del_deposito"):
            obj = obj.filter(
                anno_del_deposito__contains=request.GET["anno_del_deposito"]
            )

        if request.GET.get("sede_tribunale"):
            obj = obj.filter(
                sede_tribunale__comune__icontains=request.GET["sede_tribunale"]
            )

        # Ricerca testuale nell'OCR che supporta virgolette, DA TESTARE
        if request.GET.get("contenuto_testuale"):
            query = request.GET["contenuto_testuale"]
            chunks = query.split('"')
            full_matches = chunks[1::2]  # Elementi dispari son tra virgolette
            normal_matches = chunks[
                0::2
            ]  # Si lo so che fa cagare e non funziona sempre
            for full_match in full_matches:
                obj = obj.filter(ocr__icontains=full_match.strip())
            for normal_match in normal_matches:
                for word in normal_match.split():
                    obj = obj.filter(ocr__icontains=word.strip())

        if request.GET.get("parola_chiave"):
            trend_id = request.GET["parola_chiave"]
            if trend_id != "":
                containers = TrendProfiloRilevanteContainer.objects.filter(
                    trend__id=trend_id
                )
                profili = request.GET.getlist("profili_rilevanti")
                if len(profili) > 0:
                    containers = containers.filter(profili_rilevanti__id__in=profili)
                obj = obj.filter(trendprofilorilevantecontainer__in=containers)

        if request.GET.get("responsabilita"):
            obj = obj.filter(responsabilita=request.GET["responsabilita"])
        if "ante_2001" not in request.GET:
            obj = (
                obj.filter(anno_del_deposito__gte=2001)
                | obj.filter(data_del_deposito__gte="2001-01-01")
                | obj.filter(data_della_sentenza__gte="2001-01-01")
            )
        if not request.user.is_staff:
            obj = obj.filter(forza_esclusione=False)

        obj = obj.order_by("-data_del_deposito")

    except ValidationError as e:
        mess = (
            "Hai inserito una ricerca non valida:<br/><strong>"
            + "<br/>".join(map(html.escape, e.messages))
            + "</strong>"
        )
        return render(request, "errore.html", {"mess": mess})

    else:
        return do_paging_response(request, obj, "odp/s_results.html")

s_results = check_auth(s_results)
