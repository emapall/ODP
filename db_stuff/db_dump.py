# -*- coding: utf-8 -*-

#! /usr/bin/python
# funzione che mi crea il dict degli oggetti senza file
"""
struttura: {
 name --> nome del modello
    "name":[ # (names of models are unique)
                { # each dict is an instance of the model
                    - as many key:value as the model coloumns  
                        <filed name>:str or json serializabile
                    - and a key, value pair like
                        "old_pk": int, the old pk
                }, # each dict is an instance of the model
    ] # each model a list of instances
 }
possible model field types
- int, string or jsonizabile, just write it
- date, print with appropriate format
- file....filename?
- foreignkey, old referenced's obj pk

NOTA:
    try:
        obj = getattr(sfs, field)
    except AttributeError:
        obj = None"""

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import simplejson,html
from django.views.decorators.cache import cache_page
from lider.odp.models import *
# from odp_app.models import *
import random


def write_rule(field,t):
    if t == "int":
        try:
            return int(field)
        except:
            assert(field == None)
            return None
    if t == "str":
        return field #may be none, '' or else
    if t == "date":
        try:
            return field.strftime("%Y%m%d")
        except:
            assert(field == None)
            return None
    if t == "file":
        try:
            if "sir_tiff/2001_12136" in field.path:
                print("sir sgualdreffo trovato!!!!!!")
                input()
                return None
            return field.path #IT'S A STR!!!
        except ValueError:
            return None
    if t == "foreignkey":
        try:
            return int(field.pk)
        except:
            assert(field == None)
    if t == "bool":
        return field # may be none

def populate_model_dict(model_dict,model_name, scaledown = None):
    m_obj = model_dict["model_obj"] #class oject of the specific model
    instances_list = [] # list of instances ( == db rows) of the model
    # each instance is a dict of field_name:field_value for the various fields
    object_list = m_obj.objects.all() # list of the instances already in the db
    for m_inst in object_list:  # m_inst model instance
        if scaledown is not None: # cut the test db down
            if random.random() >= 1.0/scaledown:
                print "not saving, random"
                continue
        
        instance_dict={}  # each instance is a dict of field_name:field_value
        for fieldname, t in model_dict["fields_dict"].items():
            # print(model_name,":",fieldname)
            try:
                field = getattr(m_inst, fieldname) # get the value of the field for that instance
            except:
                assert(False)
            assert(fieldname not in instance_dict)
            # print "provo a salvare field", fieldname,t,field
            # raw_input()
            instance_dict.update({fieldname:write_rule(field,t)})
        instance_dict.update({"old_pk":int(m_inst.pk)})
        instances_list.append(instance_dict) 
        print "Saved ",m_inst, "with pk",m_inst.pk
    dump_dict.update({model_name:instances_list})

dump_dict = {}

def group1():
    models_list = [
        ("Regione",Regione),
        ("Provincia",Provincia),
        ("Comune",Comune),
        ("Esaminatore",Esaminatore),
        ("Osservatorio",Osservatorio),
        ("Assicurazione",Assicurazione),
        ("Provenienza",Provenienza),
        ("Responsabilita",Responsabilita),
    ]

    return models_list

def group2():
    models_list = [
        ("Sentenza",Sentenza),
    ]

    return models_list

def save_group(ng, scaledown = None):
    handle_dict = {
        1:group1,
        2:group2,
    }
    handle=handle_dict[ng]
    models_list = handle()
    models_dict = {m_name:models_dict_complete[m_name] for (m_name,m_obj) in models_list}
    for m_name,m_dict in models_dict.items():
        print("----------------------------INIZIO MODELLO",m_name,scaledown)
        populate_model_dict(m_dict,m_name,scaledown)
        print("----------------------------FINITO MODELLO",m_dict)
        raw_input()



models_dict_complete = {
        "Regione":{
            "model_obj":Regione,
            "fields_dict":{
                "regione":"str",
            },
        }, 
        "Provincia":{
            "model_obj":Provincia,
            "fields_dict":{
                "regione":"foreignkey",
                # "regione_name":"Regione",
                "provincia":"str",
                "targa":"str",
            },
        },
        "Comune":{
            "model_obj":Comune,
            "fields_dict":{
                "provincia":"foreignkey",
                # "provincia_name":"Provincia",
                "comune":"str",
                "codice":"str",
            },
        },
        "Esaminatore":{
            "model_obj":Esaminatore,
            "fields_dict":{
                "esaminatore":"str",
            },
        },
        "Osservatorio":{
            "model_obj":Osservatorio,
            "fields_dict":{
                "osservatorio":"str",
            },
        },
        "Assicurazione":{
            "model_obj":Assicurazione,
            "fields_dict":{
                "assicurazione":"str",
            },
        },
        "Provenienza":{
            "model_obj":Provenienza,
            "fields_dict":{
                "provenienza":"str",
            },
        },
        "Responsabilita":{
            "model_obj":Responsabilita,
            "fields_dict":{
                "responsabilita":"str",
            },
        }, 
        "Sentenza":{
            "model_obj":Sentenza,
            "fields_dict":{
                "provenienza":"foreignkey",
                # "provenienza_name":"Provenienza",
                "responsabilita":"foreignkey",
                # "responsabilita_name":"Responsabilita",
                "anno_del_deposito":"int",
                "anno_di_arrivo":"int",
                "codice":"str",
                "data_del_deposito":"date",
                "data_del_fatto":"date",
                "data_della_citazione":"date",
                "data_della_sentenza":"date",
                "estctu":"bool",
                "estensore":"str",
                "fatto":"str",
                "file_cmn":"file",
                "file_img":"file",
                "file_sch":"file",
                "forza_esclusione":"bool",
                "grado_di_giudizio":"str",
                "note_profili_rilevanti":"str",
                "note_sentenza":"str",
                "numero_attori":"int",
                "numero_convenuti":"int",
                "numero_della_sentenza":"int",
                "numero_della_sezione":"int",
                "numero_terzi":"int",
                "ocr":"str",
                "riconvenzionale":"str",
            },
        },
}
