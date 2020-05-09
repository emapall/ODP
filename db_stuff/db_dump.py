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


INFORTUNATO_BLACKLIST = [3625, 4658, 4684, 4685, 5221, 5284, 5295, 5310, 5333,]

def write_rule(fieldval,t):
    if fieldval is None :
        return None
    
    if t == "int":
        try:
            return int(fieldval)
        except:
            assert(fieldval == None)
            return None
    if t == "dec":
        try:
            return str(Decimal(fieldval))
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
                raw_input()
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

def scale_down(full_list,scaledown):
    global ng
    
    if scaledown is None and ng != 4:
        return full_list
    
    
    object_list = []
    if ng == 2:
        for o in full_list:
            if random.random() <= 1.0/scaledown:
                object_list.append(o)
        return object_list

    if ng == 4:
        if scaledown is None:
            for o in full_list:
                if o.pk not in INFORTUNATO_BLACKLIST:
                    object_list.append(o)
            return object_list

        # read the pk and check if infortunato is in the sentenze's
        pk_file = open("pk_remap.json","r")
        pk_remap_json = json.load(pk_file) # Le chiavi sono str!
        pk_remap = {"Sentenza":{}}
        # create the pk remap dict
        for k, v in pk_remap_json["Sentenza"].items():
            pk_remap["Sentenza"].update({int(k):v})
        print("Sentenza-pk:",pk_remap)
        for o in full_list:
            if o.pk in INFORTUNATO_BLACKLIST:
                continue
            if o.sentenza.pk in pk_remap["Sentenza"].keys():
                object_list.append(o)
        print("Finito scaldown infortunato,",object_list)
        raw_input()
        return object_list
    
    return full_list





def populate_model_dict(model_dict,model_name, scaledown = None):
    m_obj = model_dict["model_obj"] #class oject of the specific model
    instances_list = [] # list of instances ( == db rows) of the model
    # each instance is a dict of field_name:field_value for the various fields
    object_list = m_obj.objects.all() # list of the instances already in the db
    object_list = scale_down(object_list,scaledown)
    for m_inst in object_list:  # m_inst model instance        
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

def group4():
    return [
        "Infortunato",
    ]

def save_group(ngr, scaledown = None):
    global ng
    ng = ngr
    handle_dict = {
        1:group1,
        2:group2,
        3:group3,
        4:group4,
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
        print("m_name",m_name,"keys:",models_dict[m_name].keys())
        print("----------------------------FINITO MODELLO",m_name)
        raw_input()

    out = open("gruppo"+str(ng)+".json","w")
    json.dump(dump_dict,out)
    out.close()

global ng

file_models_dict = open("models_dict.py","r")
exec(file_models_dict)