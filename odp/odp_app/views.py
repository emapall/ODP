# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import simplejson,html
from django.views.decorators.cache import cache_page
from lider.odp.models import *

formato_date = 'j/m/Y'
base_url = '/database/odp'
search_url = base_url + '/search/'
var_login_url = base_url + '/login/'


def do_paging_response(request, obj, template):
	# default

	pag = {}
	query = {}
	
	pag['da'] = 1
	pag['quante'] = 20
	
	# prendi i dati dalla richiesta
	
	if (request.GET.has_key('quante') and request.GET['quante']):
		pag['quante'] = int(request.GET['quante'])
	elif (request.COOKIES.has_key('quante')):
		pag['quante'] = int(request.COOKIES['quante'])
	if (request.GET.has_key('inizia_da') and request.GET['inizia_da']):
		pag['da'] = int(request.GET['inizia_da'])

	# controlli

	if pag['da'] == 1:                # è la prima
		pag['precedente'] = 0
	else:
		pag['precedente'] = pag['da'] - pag['quante']
		if pag['precedente'] < 1:
			pag['precedente'] = 1

	pag['a'] = pag['da'] + pag['quante'] - 1

	if pag['a'] >= obj.count():  # è l'ultima
		pag['a'] = obj.count()
		pag['prossima'] = 0
	else:
		pag['prossima'] = pag['da'] + pag['quante']
		
	pag['totali'] = obj.count()
	
	obj = obj[pag['da']-1:pag['a']]
	
	for unaquery in request.GET.items():
		if unaquery[1] != '' and unaquery[0] != 'quante' and unaquery[0] != 'inizia_da':
			query[unaquery[0]] = unaquery[1]

	resp = render_to_response(template,{'obj':obj, 'query':query, 'pag':pag}, context_instance=RequestContext(request))
	if (not request.COOKIES.has_key('quante')) or (pag['quante'] != request.COOKIES['quante']):
		resp.set_cookie('quante', value=pag['quante'], max_age=1892160000)

	return resp


def new_s_results(request):
	# TODO add column for matched infortunati
	par_sentenza = [
			'contenuto_testuale', 'grado_di_giudizio', 'sede_tribunale',
			'data_della_sentenza', 'numero_della_sentenza',
			'data_del_deposito', 'anno_del_deposito'
			]
	par_danneggiato = [
			'est_it', 'perc_ip_min', 'perc_ip_max',
			'est_dm', 'danno_morte', 'danno_np', 'danno_p', 'metodo_dm',
			'diritti_lesi', 'trend_liq', 'eta_danneggiato'
			]
	if not any([request.GET.has_key(par) and request.GET[par] for par in par_danneggiato]):
		# Se non ci son filtri sui danneggiati considerala una ricerca sentenze
		return s_results(request)
	#TODO (per ora copio s_results
	from django.core.exceptions import ValidationError
	obj = Infortunato.objects.all()
	try:
		if (request.GET.has_key('eta_danneggiato') and request.GET['eta_danneggiato']):
			obj = obj.filter(eta=request.GET['eta_danneggiato'])
		if(request.GET.has_key('perc_ip_min') and request.GET['perc_ip_min']):
			obj = obj.filter(percentuale_das_ip__gte=request.GET['perc_ip_min'])
		if(request.GET.has_key('perc_ip_max') and request.GET['perc_ip_max']):
			obj = obj.filter(percentuale_das_ip__lte=request.GET['perc_ip_max'])
		if(request.GET.has_key('est_it')): obj = obj.filter(est_it=True)
		if(request.GET.has_key('est_dm')): obj = obj.filter(est_dm=True)
		if(request.GET.has_key('danno_morte')): obj = obj.filter(dm_est=True)
		if(request.GET.has_key('danno_np')): obj = obj.filter(sunt_diritti_lesi=True)
		if(request.GET.has_key('metodo_dm')):
			metodo = request.GET['metodo_dm']
			if metodo == "equi":
				obj = obj.filter(est_dm_vp=True)
			elif metodo == "perma":
				obj = obj.filter(est_dm_ip=True)
			elif metodo == "temp":
				obj = obj.filter(est_dm_it=True)

		if(request.GET.has_key('trend_liq')):
			trend = request.GET['trend_liq']
			if trend != '':
				obj = obj.filter(trend_liquidazione__id=trend)

		if(request.GET.has_key('diritti_lesi')):
			diritto = request.GET['diritti_lesi']
			if diritto != '':
				obj = obj.filter(dirittoinviolabile__id=diritto)

		if(request.GET.has_key('danno_p')):
			obj = obj.filter(est_ss=True) | obj.filter(est_ss_future=True) | obj.filter(dannopatrimoniale=True)
			#TODO testare

		#Attributi della sentenza (probabilmente basta mettere sentenza__)
		if(request.GET.has_key('grado_di_giudizio') and request.GET['grado_di_giudizio']):
			obj = obj.filter(sentenza__grado_di_giudizio__contains=request.GET['grado_di_giudizio'])
		if(request.GET.has_key('data_della_sentenza') and request.GET['data_della_sentenza']):
			obj = obj.filter(sentenza__data_della_sentenza=request.GET['data_della_sentenza'])
		if(request.GET.has_key('data_del_deposito') and request.GET['data_del_deposito']):
			obj = obj.filter(sentenza__data_del_deposito=request.GET['data_del_deposito'])
		if(request.GET.has_key('numero_della_sentenza') and request.GET['numero_della_sentenza']):
			obj = obj.filter(sentenza__numero_della_sentenza=request.GET['numero_della_sentenza'])
		if(request.GET.has_key('anno_del_deposito') and request.GET['anno_del_deposito']):
			obj = obj.filter(sentenza__anno_del_deposito__contains=request.GET['anno_del_deposito'])
		if(request.GET.has_key('sede_tribunale') and request.GET['sede_tribunale']):
			obj = obj.filter(sentenza__sede_tribunale__comune__icontains=request.GET['sede_tribunale'])
	
		# Ricerca testuale nell'OCR che supporta virgolette, DA SISTEMARE (matchare le parole)
		if(request.GET.has_key('contenuto_testuale') and request.GET['contenuto_testuale']):
			query = request.GET['contenuto_testuale']
			chunks = query.split('"')
			full_matches = chunks[1::2] # Elementi dispari son tra virgolette
			normal_matches = chunks[0::2] # Si lo so che fa cagare e non funziona sempre
			for full_match in full_matches:
				obj = obj.filter(sentenza__ocr__icontains=full_match.strip())
			for normal_match in normal_matches:
				for word in normal_match.split():
					obj = obj.filter(sentenza__ocr__icontains=word.strip())

		obj = obj.order_by('-sentenza__data_del_deposito')

	
	except ValidationError, e:
		mess = 'Hai inserito una ricerca non valida:<br/><strong>'+ '<br/>'.join(map(html.escape,e.messages)) +'</strong>'
		return render_to_response('errore.html', {'mess':mess}, context_instance=RequestContext(request))
	else:
		return do_paging_response(request, obj, 'odp/i_results.html')

	
def s_results(request):
	from django.core.exceptions import ValidationError
	obj = Sentenza.objects.all()
	
	try:
		if(request.GET.has_key('grado_di_giudizio') and request.GET['grado_di_giudizio']):
			obj = obj.filter(grado_di_giudizio__contains=request.GET['grado_di_giudizio'])
		if(request.GET.has_key('data_della_sentenza') and request.GET['data_della_sentenza']):
			obj = obj.filter(data_della_sentenza=request.GET['data_della_sentenza'])
		if(request.GET.has_key('data_del_deposito') and request.GET['data_del_deposito']):
			obj = obj.filter(data_del_deposito=request.GET['data_del_deposito'])
		if(request.GET.has_key('numero_della_sentenza') and request.GET['numero_della_sentenza']):
			obj = obj.filter(numero_della_sentenza=request.GET['numero_della_sentenza'])
		if(request.GET.has_key('estensore') and request.GET['estensore']):
			obj = obj.filter(estensore__contains=request.GET['estensore'])
		if(request.GET.has_key('anno_del_deposito') and request.GET['anno_del_deposito']):
			obj = obj.filter(anno_del_deposito__contains=request.GET['anno_del_deposito'])

		if(request.GET.has_key('sede_tribunale') and request.GET['sede_tribunale']):
			obj = obj.filter(sede_tribunale__comune__icontains=request.GET['sede_tribunale'])

		# Ricerca testuale nell'OCR che supporta virgolette, DA TESTARE
		if(request.GET.has_key('contenuto_testuale') and request.GET['contenuto_testuale']):
			query = request.GET['contenuto_testuale']
			chunks = query.split('"')
			full_matches = chunks[1::2] # Elementi dispari son tra virgolette
			normal_matches = chunks[0::2] # Si lo so che fa cagare e non funziona sempre
			for full_match in full_matches:
				obj = obj.filter(ocr__icontains=full_match.strip())
			for normal_match in normal_matches:
				for word in normal_match.split():
					obj = obj.filter(ocr__icontains=word.strip())

		if(request.GET.has_key('parola_chiave')):
			trend_id = request.GET['parola_chiave']
			if trend_id != "":
				containers = TrendProfiloRilevanteContainer.objects.filter(trend__id=trend_id)
				profili = request.GET.getlist('profili_rilevanti')
				if len(profili)>0:
					containers = containers.filter(profili_rilevanti__id__in=profili)
				obj = obj.filter(trendprofilorilevantecontainer__in=containers)

		if(request.GET.has_key('responsabilita') and request.GET['responsabilita']):
			obj = obj.filter(responsabilita=request.GET['responsabilita'])
		if(not request.GET.has_key('ante_2001')):
			obj = obj.filter(anno_del_deposito__gte = 2001) | obj.filter(data_del_deposito__gte = "2001-01-01") | obj.filter(data_della_sentenza__gte = "2001-01-01")
		if(not request.user.is_staff):
			obj = obj.filter(forza_esclusione=False)

		obj = obj.order_by('-data_del_deposito')

	except ValidationError, e:
		mess = 'Hai inserito una ricerca non valida:<br/><strong>'+ '<br/>'.join(map(html.escape,e.messages)) +'</strong>'
		return render_to_response('errore.html', {'mess':mess}, context_instance=RequestContext(request))
	
	else:
		return do_paging_response(request, obj, 'odp/s_results.html')



def s_details(request):
	if(request.GET.has_key('id')):
		from django.core.exceptions import ObjectDoesNotExist
		
		try:
			sent_id = int(request.GET['id'])
		except ValueError:
			return render_to_response('errore.html', {'redir':search_url, 'mess':"Richiesta non valida."}, context_instance=RequestContext(request))

		try:
			sent = Sentenza.objects.get(id__exact = sent_id)
		except ObjectDoesNotExist:
			return render_to_response('errore.html', {'redir':search_url, 'mess':"Non esiste una sentenza con questo ID. Se hai salvato questo indirizzo, potrebbe essere stata cancellata o spostata. Per favore esegui di nuovo la ricerca."}, context_instance=RequestContext(request))
		else:	
			suoi_infortunati = sent.infortunati.all()
			cont = TrendProfiloRilevanteContainer.objects.filter(sentenza=sent)
			if (not request.user.is_staff):
				if (sent.forza_esclusione):
					return render_to_response('errore.html', {'mess':"Questa scheda sentenza non &egrave; ancora pronta per la pubblicazione.", 'redir':request.META['HTTP_REFERER']}, context_instance=RequestContext(request))
			if (not request.user.is_staff):
				for uninfortunato in suoi_infortunati:
					if (not uninfortunato.pubblicabile):
						return render_to_response('errore.html', {'mess':"Questa scheda sentenza non &egrave; ancora pronta per la pubblicazione.", 'redir':request.META['HTTP_REFERER']}, context_instance=RequestContext(request))
			return render_to_response('odp/s_details.html', {'sent':sent, 'cont':cont,'formato_date':formato_date}, context_instance=RequestContext(request))
	
	else:
		return HttpResponsePermanentRedirect(search_url)



def i_results(request):
	from django.core.exceptions import ValidationError
	from django.utils.html import escape
	obj = Infortunato.objects.all()
	
	try:
		if(request.GET.has_key('eta') and request.GET['eta']): obj = obj.filter(eta=request.GET['eta'])
		if(request.GET.has_key('est_maggiorenne') and request.GET['est_maggiorenne']):
			obj = obj.filter(est_maggiorenne=request.GET['est_maggiorenne'])
			if (request.GET['est_maggiorenne'] == 0):
				obj = obj.filter(eta<18);

		if(request.GET.has_key('sesso') and request.GET['sesso']): obj = obj.filter(sesso=request.GET['sesso'])
		if(request.GET.has_key('professione') and request.GET['professione']):
			obj = obj.filter(professione=request.GET['professione'])
		if(request.GET.has_key('lesione')  and request.GET['lesione']):
			nobj = obj.filter(id=(-1))
			for unalesione in request.GET.getlist('lesione'):
				nobj = nobj | obj.filter(lesione=unalesione)
			obj = nobj
		if(request.GET.has_key('postumo')  and request.GET['postumo']):
			nobj = obj.filter(id=(-1))
			for unpostumo in request.GET.getlist('postumo'):
				nobj = nobj | obj.filter(postumo=unpostumo)
			obj = nobj
		if(not request.GET.has_key('ante_2001')):
			obj = obj.filter(pre2001=False)
		if(not request.user.is_staff):
			obj = obj.filter(pubblicabile=True)
	
	except ValidationError, e:
		mess = 'Hai inserito una ricerca non valida:<br/><strong>'+ '<br/>'.join(map(html.escape,e.messages)) +'</strong>'
		return render_to_response('errore.html', {'mess':mess}, context_instance=RequestContext(request))
	
	else:
		return do_paging_response(request, obj, 'odp/i_results.html')



def i_details(request):
	if(request.GET.has_key('id')):
		from django.core.exceptions import ObjectDoesNotExist

		try:
			infort_id = int(request.GET['id'])
		except ValueError:
			return render_to_response('errore.html', {'redir':search_url, 'mess':"Richiesta non valida."}, context_instance=RequestContext(request))		

		try:
			infort = Infortunato.objects.get(id__exact = infort_id)
		except ObjectDoesNotExist:
			return render_to_response('errore.html',{'redir':search_url, 'mess':"Non esiste un infortunato con questo ID. Se hai salvato questo indirizzo, potrebbe essere stato cancellato o spostato. Per favore esegui di nuovo la ricerca."}, context_instance=RequestContext(request))
		
		return render_to_response('odp/i_details.html', {'infort':infort,'formato_date':formato_date}, context_instance=RequestContext(request))
	else:
		return HttpResponsePermanentRedirect(search_url)



def d_results(request):
	from django.core.exceptions import ValidationError
	from django.utils.html import escape
	obj = Infortunato.objects.all()
	
	try:
		if(request.GET.has_key('perc_ip_da') and request.GET['perc_ip_da']):
			obj = obj.filter(percentuale_das_ip__gte=request.GET['perc_ip_da'])
		if(request.GET.has_key('perc_ip_a') and request.GET['perc_ip_a']):
			obj = obj.filter(percentuale_das_ip__lte=request.GET['perc_ip_a'])
		
		if(request.GET.has_key('metodo_das_ip') and request.GET['metodo_das_ip']):
			obj = obj.filter(metodo_das_ip=request.GET['metodo_das_ip'])
		
		if(request.GET.has_key('sede_tabella')): obj = obj.filter(sede_tabella=request.GET['sede_tabella'])

		if(request.GET.has_key('est_clg')): obj = obj.filter(est_clg=True)
		if(request.GET.has_key('est_cls')): obj = obj.filter(est_cls=True)

		if(request.GET.has_key('est_lcip')): obj = obj.filter(est_lcip=True)

		if(request.GET.has_key('est_it')): obj = obj.filter(est_it=True)
		if(request.GET.has_key('metodo_das_it') and request.GET['metodo_das_it']):
			obj = obj.filter(metodo_das_it=request.GET['metodo_das_it'])

		if(request.GET.has_key('est_lcit')): obj = obj.filter(est_lcit=True)

		if(request.GET.has_key('est_dm')): obj = obj.filter(est_dm=True)
		if(request.GET.has_key('metodo_dm')): 
			metodo = request.GET['metodo_dm']
			if metodo == "equi":
				obj = obj.filter(est_dm_vp=True)
			elif metodo == "perma":
				obj = obj.filter(est_dm_ip=True)
			elif metodo == "temp":
				obj = obj.filter(est_dm_it=True)

		if(request.GET.has_key('danno_np')): obj = obj.filter(sunt_diritti_lesi=True)
		if(request.GET.has_key('diritti_lesi')): 
			diritto = request.GET['diritti_lesi']
			if diritto != '':
				obj = obj.filter(dirittoinviolabile__id=diritto)
			
				
		if(request.GET.has_key('danno_morte')): obj = obj.filter(dm_est=True)

		if(request.GET.has_key('danno_p')): 
			danno = request.GET['danno_p']
			if danno == "spese_sostenute":
				obj = obj.filter(est_ss=True)
			elif metodo == "spese_future":
				obj = obj.filter(est_ss_future=True)
			#TODO altri danni come fare??

		if(request.GET.has_key('trend_liq')): 
			trend = request.GET['trend_liq']
			if trend != '':
				obj = obj.filter(trend_liquidazione__id=trend)

		if(not request.GET.has_key('ante_2001')):
			obj = obj.filter(pre2001=False)
	
	except ValidationError, e:
		mess = 'Hai inserito una ricerca non valida:<br/><strong>'+ '<br/>'.join(map(html.escape,e.messages)) +'</strong>'
		return render_to_response('errore.html', {'mess':mess}, context_instance=RequestContext(request))
	
	else:
		return do_paging_response(request, obj, 'odp/i_results.html')


def new_search(request):
	return render_to_response('odp/tmp_search.html',{},context_instance=RequestContext(request)) 

###### /search_ns: ricerca noscript ############

def search_noscript(request):
	assicurazioni = Assicurazione.objects.all()
	lesioni = Lesione.objects.all()
	postumi = Postumo.objects.all()
	professioni = Professione.objects.all()
	responsabilita = Responsabilita.objects.all()
	return render_to_response('odp/search_noscript.html', {'assicurazioni':assicurazioni, 'lesioni':lesioni, 'postumi':postumi, 'professioni':professioni}, context_instance=RequestContext(request))
	

###### /search: ricerca ########################

def search(request):
	responsabilita = Responsabilita.objects.all()
	diritti_lesi = DirittoInviolabile.objects.all()
	trend_liq = TrendLiquidazione.objects.all() 
	parole_chiave = TrendProfiloRilevante.objects.all()
	return render_to_response('odp/search.html', 
			{
				'responsabilita':responsabilita,
				'diritti_lesi':diritti_lesi,
				'trend_liq':trend_liq,
				'parole_chiave':parole_chiave,
			}, 
			context_instance=RequestContext(request))


############## AJAX da /search #################

@cache_page(2 * 60 * 60) # cachea la json per 2 ore
def json_assicurazioni(request):
	dati = Assicurazione.objects.all()
	return HttpResponse(
		simplejson.dumps(tuple(dati.values()), ensure_ascii=False), 
		content_type = 'application/json; charset=UTF-8' )

@cache_page(2 * 60 * 60)
def json_professioni(request):
	dati = Professione.objects.all()
	return HttpResponse(
		simplejson.dumps(tuple(dati.values()), ensure_ascii=False), 
		content_type = 'application/json; charset=UTF-8' )

@cache_page(2 * 60 * 60)
def json_lesioni(request):
	dati = Lesione.objects.all()
	return HttpResponse(
		simplejson.dumps(tuple(dati.values()), ensure_ascii=False), 
		content_type = 'application/json; charset=UTF-8' )

@cache_page(2 * 60 * 60)
def json_postumi(request):
	dati = Postumo.objects.all()
	return HttpResponse(
		simplejson.dumps(tuple(dati.values()), ensure_ascii=False), 
		content_type = 'application/json; charset=UTF-8' )

@cache_page(2 * 60 * 60)
def json_profili_rilevanti(request):
	trend_id = request.GET.get('id','-1')
	trend_id = int(trend_id)
	
	dati = ProfiloRilevante.objects.all()
	dati = dati.filter(trend__id=trend_id) 
	return HttpResponse(
		simplejson.dumps(tuple(dati.values()), ensure_ascii=False), 
		content_type = 'application/json; charset=UTF-8' )

###### autenticazione ##########################

def logout_view(request):
	from django.contrib.auth import logout
	from django.http import HttpResponseRedirect
	
	logout(request)
	return HttpResponseRedirect(search_url)
	
def singup(request):
	from django.http import HttpResponseRedirect
	from lider.odp.forms import SignUpForm
	from lider.odp.tokens import account_activation_token
	from django.template.loader import render_to_string
	from django.utils.http import urlsafe_base64_encode
	from django.utils.encoding import force_bytes
	
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			current_domain = 'www.lider-lab.sssup.it'
			subject = "Attiva il tuo Account ODP"
			message = render_to_string('odp/account_activation_email.html', {
				'user': user,
				'domain': current_domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user)
				})
			user.email_user(subject, message)
			return HttpResponseRedirect(base_url + '/account_activation_sent/')
	else:
		form = SignUpForm()
	return render(request, 'odp/signup.html', {'form': form})

def activate(request, uidb64, token):
	from django.http import HttpResponseRedirect
	from django.contrib.auth.models import User
	from django.shortcuts import render, redirect
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
		return render(request, 'account_activation_invalid.html')

def account_activation_sent(request):
	return render(request, 'odp/account_activation_sent.html')

s_results =          user_passes_test(lambda u: u.is_authenticated(), login_url=var_login_url)(s_results)
new_s_results =          user_passes_test(lambda u: u.is_authenticated(), login_url=var_login_url)(new_s_results)
s_details =          user_passes_test(lambda u: u.is_authenticated(), login_url=var_login_url)(s_details)
i_results =          user_passes_test(lambda u: u.is_authenticated(), login_url=var_login_url)(i_results)
i_details =          user_passes_test(lambda u: u.is_authenticated(), login_url=var_login_url)(i_details)
d_results =          user_passes_test(lambda u: u.is_authenticated(), login_url=var_login_url)(d_results)
search_noscript =    user_passes_test(lambda u: u.is_authenticated(), login_url=var_login_url)(search_noscript)
search =             user_passes_test(lambda u: u.is_authenticated(), login_url=var_login_url)(search)
new_search =         user_passes_test(lambda u: u.is_authenticated(), login_url=var_login_url)(new_search)
