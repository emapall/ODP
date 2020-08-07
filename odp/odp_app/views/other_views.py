# -*- coding: utf-8 -*-
import json

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.utils import html
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError

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

formato_date = "j/m/Y"
base_url = "odp" # TODO: DECIDE WITH URLS AND STUFF!
search_url = base_url + "/search/"
var_login_url = base_url + "/login"


def do_paging_response(request, obj, template):
    # default

    pag = {}
    query = {}

    pag["da"] = 1
    pag["quante"] = 20

    # prendi i dati dalla richiesta

    if request.GET.get("quante"):
        pag["quante"] = int(request.GET["quante"])
    elif request.COOKIES.get("quante"):
        pag["quante"] = int(request.COOKIES["quante"])
    if request.GET.get("inizia_da"):
        pag["da"] = int(request.GET["inizia_da"])

    # controlli

    if pag["da"] == 1:  # è la prima
        pag["precedente"] = 0
    else:
        pag["precedente"] = pag["da"] - pag["quante"]
        if pag["precedente"] < 1:
            pag["precedente"] = 1

    pag["a"] = pag["da"] + pag["quante"] - 1

    if pag["a"] >= obj.count():  # è l'ultima
        pag["a"] = obj.count()
        pag["prossima"] = 0
    else:
        pag["prossima"] = pag["da"] + pag["quante"]

    pag["totali"] = obj.count()

    obj = obj[pag["da"] - 1 : pag["a"]]

    for unaquery in request.GET.items():
        if unaquery[1] != "" and unaquery[0] != "quante" and unaquery[0] != "inizia_da":
            query[unaquery[0]] = unaquery[1]

    resp = render(request, template, {"obj": obj, "query": query, "pag": pag})
    if (not request.COOKIES.get("quante")) or (
        pag["quante"] != request.COOKIES["quante"]
    ):
        resp.set_cookie("quante", value=pag["quante"], max_age=1892160000)

    return resp

@login_required
def s_results(request):
    """
        Praticamente è uguale a new_s_results, ma 
        - manca tutta la parte di filtraggio sugli infortunati
        - ci sono cose aggiuntive come parole_chiave, ante_2001, profili rilevanti
        - praticamente tutta sta roba è stata sostituita da contesto testuale e basta (ma è giusto?)
    """
    """
        Same concept as new_s_results, but improved filtering for Sentenza
        rather than Infortunato 
    """
    from django.core.exceptions import ValidationError

    obj = Sentenza.objects.all()
    print(request.GET)
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
        
        # TODO 
        if "ante_2001" not in request.GET:
            obj = (
                obj.filter(anno_del_deposito__gte=2001)
                | obj.filter(data_del_deposito__gte="2001-01-01")
                | obj.filter(data_della_sentenza__gte="2001-01-01")
            ) 
        # https://docs.djangoproject.com/en/3.0/ref/models/querysets/#or
        if not request.user.is_staff:
            obj = obj.filter(forza_esclusione=False) # false perchè forza esclusione
            # se è true allora va esclusa

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

@login_required
def new_s_results(request):
    # TODO add column for matched infortunati

    # par_sentenza = [
    #    "contenuto_testuale",
    #    "grado_di_giudizio",
    #    "sede_tribunale",
    #    "data_della_sentenza",
    #    "numero_della_sentenza",
    #    "data_del_deposito",
    #    "anno_del_deposito",
    # ]

    par_danneggiato = [
        "est_it",
        "perc_ip_min",
        "perc_ip_max",
        "est_dm",
        "danno_morte",
        "danno_np",
        "danno_p",
        "metodo_dm",
        "diritti_lesi",
        "trend_liq",
        "eta_danneggiato",
    ]
    if not any([request.GET.get(par) for par in par_danneggiato]):
        # Se non ci son filtri sui danneggiati considerala una ricerca sentenze
        return s_results(request)

    # TODO (per ora copio s_results)
    # TODO USE par_danneggiato maybe? (or maybe not)
    
    obj = Infortunato.objects.all()
    try:
        if request.GET.get("eta_danneggiato"):
            obj = obj.filter(eta=request.GET["eta_danneggiato"])
        # invalidità permanente - min and max
        if request.GET.get("perc_ip_min"):  # 0 equals no filter
            obj = obj.filter(percentuale_das_ip__gte=request.GET["perc_ip_min"])
        if request.GET.get("perc_ip_max"):  # TODO 0?
            obj = obj.filter(percentuale_das_ip__lte=request.GET["perc_ip_max"])
        # TODO: DOES NOT EXISTS IN HTML
        if "est_id" in request.GET:
            obj = obj.filter(est_it=True)
        # danno morale
        if "est_dm" in request.GET:
            obj = obj.filter(est_dm=True)
        # danno morte
        if "danno_morte" in request.GET:
            obj = obj.filter(dm_est=True)
        # TODO DOES NOT EXISTS IN HTML
        if "danno_np" in request.GET:
            obj = obj.filter(sunt_diritti_lesi=True)
        # TODO NOT FOUND/HIDDEN(?)
        # dettagli danno morale (not displayed)
        if "metodo_dm" in request.GET:
            metodo = request.GET["metodo_dm"]
            if metodo == "equi":
                obj = obj.filter(est_dm_vp=True)
            elif metodo == "perma":
                obj = obj.filter(est_dm_ip=True)
            elif metodo == "temp":
                obj = obj.filter(est_dm_it=True)
        # Trendo liquidazione
        if request.GET.get("trend_liq"):  # TODO 0?
            trend = request.GET["trend_liq"]
            obj = obj.filter(trend_liquidazione__id=trend)
        # altre tipologie di danno alla persona ->
        # danno non patrimon. diverso da salute
        if request.GET.get("diritti_lesi"):
            diritto = request.GET["diritti_lesi"]
            obj = obj.filter(dirittoinviolabile__id=diritto)
        # danno patrimoniale
        if "danno_p" in request.GET:
            obj = (
                obj.filter(est_ss=True)
                | obj.filter(est_ss_future=True)
                | obj.filter(dannopatrimoniale=True)
            )
            # TODO testare TODO si testare

        # -------- SENTENZA -------- 

        # TODO: perchè c'è questa cosa che è la copia di 
        # s_results, non s possono unire le due cose?

        if request.GET.get("grado_di_giudizio"):
            obj = obj.filter(
                sentenza__grado_di_giudizio__contains=request.GET["grado_di_giudizio"]
            )
        if request.GET.get("data_della_sentenza"):
            obj = obj.filter(
                sentenza__data_della_sentenza=request.GET["data_della_sentenza"]
            )
        if request.GET.get("data_del_deposito"):
            obj = obj.filter(
                sentenza__data_del_deposito=request.GET["data_del_deposito"]
            )
        if request.GET.get("numero_della_sentenza"):
            obj = obj.filter(
                sentenza__numero_della_sentenza=request.GET["numero_della_sentenza"]
            )
        if request.GET.get("anno_del_deposito"):
            obj = obj.filter(
                sentenza__anno_del_deposito__contains=request.GET["anno_del_deposito"]
            )
        if request.GET.get("sede_tribunale"):
            sede = request.GET["sede_tribunale"]
            obj = obj.filter(sentenza__sede_tribunale__comune__icontains=sede)
        
        # Ricerca testuale nell'OCR che supporta virgolette, DA SISTEMARE (matchare le parole)
        if request.GET.get("contenuto_testuale"):
            query = request.GET["contenuto_testuale"]
            chunks = query.split('"')
            full_matches = chunks[1::2]  # Elementi dispari son tra virgolette
            normal_matches = chunks[
                0::2
            ]  # Si lo so che fa cagare e non funziona sempre
            #TODO FIX UNICODE IN OCR (?)
            for full_match in full_matches:
                obj = obj.filter(sentenza__ocr__icontains=full_match.strip())
            for normal_match in normal_matches:
                for word in normal_match.split():
                    obj = obj.filter(sentenza__ocr__icontains=word.strip())
        
        #security check
        if not request.user.is_staff: 
            obj = obj.filter(sentenza__forza_esclusione=False) # false perchè forza esclusione
            # se è true allora va esclusa

        obj = obj.order_by("-sentenza__data_del_deposito")

    except ValidationError as e:
        mess = (
            "Hai inserito una ricerca non valida:<br/><strong>"
            + "<br/>".join(map(html.escape, e.messages))
            + "</strong>"
        )
        return render(request, "errore.html", {"mess": mess})
    else: #TODO WHY USE TRY EXCEPT ELSE instead of try return except???
        return do_paging_response(request, obj, "odp/i_results.html")

@login_required
def s_details(request,sent_id):
    # if request.GET.get("id"):
    #     try:
    #         sent_id = int(request.GET["id"])
    #     except ValueError:
    #         return render(
    #             request,
    #             "errore.html",
    #             {"redir": search_url, "mess": "Richiesta non valida."},
    #         )
    # tutto il resto della funzione andrebbe indentato
    try:
        sent = Sentenza.objects.get(id__exact=sent_id)
    except ObjectDoesNotExist:
        return render(
            request,
            "errore.html",
            {
                "redir": search_url,
                "mess": "Non esiste una sentenza con questo ID. Se hai salvato questo indirizzo, potrebbe essere stata cancellata o spostata. Per favore esegui di nuovo la ricerca.",
            },
        )
    else:
        suoi_infortunati = sent.infortunati.all()
        cont = TrendProfiloRilevanteContainer.objects.filter(sentenza=sent)
        if sent.forza_esclusione and (not request.user.is_staff):
            return render(
                request,
                "errore.html",
                {
                    "mess": "Questa scheda sentenza non &egrave; ancora pronta per la pubblicazione.",
                    "redir": request.META["HTTP_REFERER"],
                },
            )
        # security check: if at LEAST 1 INFORTUNATO IS not pubblicabile, 
        # then throw an error

        # TODO: ANCHE se non si cambia, rifare bene
        if not request.user.is_staff:
            for uninfortunato in suoi_infortunati:
                if not uninfortunato.pubblicabile: # TODO: CAMBIARE COME MI HA DETTO ELEFETHRIA
                    return render(
                        request,
                        "errore.html",
                        {
                            "mess": "Questa scheda sentenza non &egrave; ancora pronta per la pubblicazione.",
                            "redir": request.META["HTTP_REFERER"],
                        },
                    )
        return render(
            request,
            "odp/s_details.html",
            {"sent": sent, "cont": cont, "formato_date": formato_date},
        )

    # else:
    #     return HttpResponsePermanentRedirect(search_url)
@login_required
def i_details(request, infort_id):
    # if request.GET.get("id"):
    #     from django.core.exceptions import ObjectDoesNotExist

    #     try:
    #         infort_id = int(request.GET["id"])
    #     except ValueError:
    #         return render(
    #             request,
    #             "errore.html",
    #             {"redir": search_url, "mess": "Richiesta non valida."},
    #         )
    # TUTTA LA ROBA SEGUENTE ANDREBBE DENTRO L'IF
    try:
        infort = Infortunato.objects.get(pk=infort_id)
    except ObjectDoesNotExist:
        return render(
            request,
            "errore.html",
            {
                "redir": search_url,
                "mess": "Non esiste un infortunato con questo ID. Se hai salvato questo indirizzo, potrebbe essere stato cancellato o spostato. Per favore esegui di nuovo la ricerca.",
            }
        )
    # TODO: la security farla qui, non nel template (pubblicabile/staff :\)
    return render(
        request,
        "odp/i_details.html",
        {"infort": infort, "formato_date": formato_date},
    )
    # else:
    #     return HttpResponsePermanentRedirect(search_url)


@login_required
def new_search(request):
    return render(request, "odp/new_search.html", {})

def test(request,schifo,schifo2):
    print(schifo,schifo2,type(schifo),type(schifo2))
###### /search_ns: ricerca noscript ############

"""
def search_noscript(request):
    assicurazioni = Assicurazione.objects.all()
    lesioni = Lesione.objects.all()
    postumi = Postumo.objects.all()
    professioni = Professione.objects.all()
    responsabilita = Responsabilita.objects.all()
    return render_to_response(
        "odp/search_noscript.html",
        {
            "assicurazioni": assicurazioni,
            "lesioni": lesioni,
            "postumi": postumi,
            "professioni": professioni,
        },
    )
"""



############## AJAX da /search #################
@cache_page(2 * 60 * 60)  # cachea la json per 2 ore
def json_assicurazioni(request):
    dati = Assicurazione.objects.all()
    return HttpResponse(
        json.dumps(tuple(dati.values()), ensure_ascii=False),
        content_type="application/json; charset=UTF-8",
    )

@cache_page(2 * 60 * 60)
def json_professioni(request):
    dati = Professione.objects.all()
    return HttpResponse(
        json.dumps(tuple(dati.values()), ensure_ascii=False),
        content_type="application/json; charset=UTF-8",
    )

@cache_page(2 * 60 * 60)
def json_lesioni(request):
    dati = Lesione.objects.all()
    return HttpResponse(
        json.dumps(tuple(dati.values()), ensure_ascii=False),
        content_type="application/json; charset=UTF-8",
    )

@cache_page(2 * 60 * 60)
def json_postumi(request):
    dati = Postumo.objects.all()
    return HttpResponse(
        json.dumps(tuple(dati.values()), ensure_ascii=False),
        content_type="application/json; charset=UTF-8",
    )

@cache_page(2 * 60 * 60)
def json_profili_rilevanti(request):
    trend_id = request.GET.get("id", "-1")
    trend_id = int(trend_id)

    dati = ProfiloRilevante.objects.all()
    dati = dati.filter(trend__id=trend_id)
    return HttpResponse(
        json.dumps(tuple(dati.values()), ensure_ascii=False),
        content_type="application/json; charset=UTF-8",
    )


###### autenticazione ##########################

def account_activation_sent(request):
    return render(request, "odp/account_activation_sent.html")

def check_auth(view_func):
    print("check aurth",view_func)
    print(user_passes_test(lambda u: u.is_authenticated,login_url=var_login_url)(view_func
    ))    
    return user_passes_test(lambda u: u.is_authenticated, login_url=var_login_url)(
        view_func
    )


# new_s_results = check_auth(new_s_results)
# s_results = check_auth(s_results)
# s_details = check_auth(s_details)
# i_details = check_auth(i_details)
"""search_noscript = user_passes_test(
    lambda u: u.is_authenticated(), login_url=var_login_url
)(search_noscript)"""
# new_search = check_auth(new_search)
