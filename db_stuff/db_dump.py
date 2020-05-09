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
import random, json
from decimal import Decimal


def write_rule(fieldval,t):
    if fieldval is None:
        return None
    
    if t == "int":
        try:
            return int(fieldval)
        except:
            assert(fieldval == None)
            return None
    if t == "dec":
        try:
            return Decimal(fieldval)
        except:
            assert(fieldval is None)
            return None
    if t == "str":
        return fieldval #may be none, '' or else
    if t == "date":
        try:
            return fieldval.strftime("%Y%m%d")
        except:
            assert(fieldval == None)
            return None
    if t == "file":
        try:
            if "sir_tiff/2001_12136" in fieldval.path:
                print("sir sgualdreffo trovato!!!!!!")
                input()
                return None
            return fieldval.path #IT'S A STR!!!
        except ValueError:
            return None
    if t == "foreignkey":
        try:
            return int(fieldval.pk)
        except:
            assert(fieldval == None)
    if t == "manytomany-d": # TODO: MANYTOMANY REVERSE
        # fieldval is then a many to many manager (.all() is queryset)
        return [ pointed_obj.pk for pointed_obj in fieldval.all() ]
    if t == "bool":
        return fieldval # may be none

    assert(False)
        
def populate_model_dict(model_dict,model_name, scaledown = None):
    m_obj = model_dict["model_obj"] #class oject of the specific model
    instances_list = [] # list of instances ( == db rows) of the model
    # each instance is a dict of field_name:field_value for the various fields
    object_list = m_obj.objects.all() # list of the instances already in the db
    for m_inst in object_list:  # m_inst model instance
        if scaledown is not None: # cut the test db down
            if random.random() >= 1.0/scaledown:
                print "not saving, random -", m_inst
                continue
        
        instance_dict={}  # each instance is a dict of field_name:field_value
        
        #save base fields
        for fieldname, t in model_dict["fields_dict"].items():
            # print(model_name,":",fieldname)
            try:
                field = getattr(m_inst, fieldname) # get the value of the field for that instance
            except:
                print fieldname
                assert(False)
            assert(fieldname not in instance_dict)
            # print "provo a salvare field", fieldname,t,field
            # raw_input()
            instance_dict.update({fieldname:write_rule(field,t)})
        # many to many
        if "many_to_many_dict" in model_dict.keys():
            for fieldname, t in model_dict["many_to_many_dict"].items():
                try:
                    field = getattr(m_inst, fieldname) # get the value of the field for that instance
                except:
                    print fieldname
                    assert(False)
                assert(fieldname not in instance_dict)
                instance_dict.update({fieldname:write_rule(field,t)})
        # files
        if "files_list" in model_dict.keys():
            for fieldname, t in model_dict["files_list"].items():
                try:
                    field = getattr(m_inst, fieldname) # get the value of the field for that instance
                except:
                    print fieldname
                    assert(False)
                assert(fieldname not in instance_dict)
                instance_dict.update({fieldname:write_rule(field,t)})

        instance_dict.update({"old_pk":int(m_inst.pk)})
        instances_list.append(instance_dict) 
        print "Saved ",m_inst, "with pk",m_inst.pk
    # endfor on object instances    
    dump_dict.update({model_name:instances_list})

dump_dict = {}

def group1():
    models_list = [
        "Regione",
        "Provincia",
        "Comune",
        "Esaminatore",
        "Osservatorio",
        "Assicurazione",
        "Provenienza",
        "Responsabilita",
    ]

    return models_list

def group2():
    models_list = [
        "Sentenza",
    ]

    return models_list

def group3():
    modes_list = [
        "Lesione",
        "Postumo",
        "Postumo_tabulato",
        "RichiestaParteAttrice",
        "DannoPatrimoniale",
        "DirittoInviolabile",
        "Professione",
        "FattoreLiquidazione",
        "FattoreLiquidazioneDP",
        "ProvaDelDNP",
        "ProvaDelDP",
        "TrendLiquidazione",
    ]    

    return models_list

    
def save_group(ngr, scaledown = None):
    global ng
    ng = ngr
    handle_dict = {
        1:group1,
        2:group2,
        3:group3,
    }
    handle=handle_dict[ng]
    models_list = handle()
    for m_name in models_list:
        print("----------------------------INIZIO MODELLO",m_name,scaledown)
        populate_model_dict(
                model_dict=models_dict[m_name],
                model_name=m_name,
                scaledown=scaledown
            )
        print("----------------------------FINITO MODELLO",m_dict)
        raw_input()

    out = open("gruppo"+str(ng)+".json","w")
    json.dump(dump_dict,out)
    out.close()

global ng

file_models_dict = open("/home/snake/models_dict.py","r")
exec(file_models_dict)