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




def write_rule(field,t):
    if t == "int":
        return int(field)
    if t == "str":
        return field
    if t == "date":
        return field.strftime("%Y%m%d")
    if t == "file":
        assert False
    if t == "foreignkey":
        return int(field.pk)

def populate_model_dict(model_dict):
    m_obj = model_dict["model_obj"] #class oject of the specific model
    m_name = model_dict["model_name"] # name of the specific model
    instances_list = [] # list of instances ( == db rows) of the model
    # each instance is a dict of field_name:field_value for the various fields
    object_list = m_obj.objects.all() # list of the instances already in the db
    for m_inst in object_list:  # m_inst model instance
        instance_dict={}  # each instance is a dict of field_name:field_value
        for (fieldname, t) in model_dict["field_list"]:
            try:
                field = getattr(m_inst, fieldname) # get the value of the field for that instance
            except:
                assert(False)
            assert(fieldname not in instance_dict)
            instance_dict.update({fieldname:write_rule(field,t)})
        instance_dict.update({"old_pk":int(m_inst.pk)})
        instances_list.append(instance_dict) 
        print "L'istanza per ",m_inst, "è",instance_dict
    dump_dict.update({m_name:instances_list})




model_dicts = [
        { # Regione
            "model_name":"Regione",
            "model_obj":Regione,
            "field_list":[
                ("regione","str"),
            ],
        }, 

        { # Provincia 
            "model_name":"Provincia",
            "model_obj":Provincia,
            "field_list":[
                ("regione","foreignkey"),
                ("provincia","str"),
                ("targa","str"),
            ],
        },

        { # Comune 
            "model_name":"Comune",
            "model_obj":Comune,
            "field_list":[
                ("provincia","foreignkey"),
                ("comune","str"),
                ("codice","str"),
            ],
        },

        { # Esaminatore 
            "model_name":"Esaminatore",
            "model_obj":Esaminatore,
            "field_list":[
                ("esaminatore","str"),
            ],
        },
        { # Osservatorio 
            "model_name":"Osservatorio",
            "model_obj":Osservatorio,
            "field_list":[
                ("osservatorio","str"),
            ],
        },

        { # Assicurazione 
            "model_name":"Assicurazione",
            "model_obj":Assicurazione,
            "field_list":[
                ("assicurazione","str"),
            ],
        },

        { # Provenienza 
            "model_name":"Provenienza",
            "model_obj":Provenienza,
            "field_list":[
                ("provenienza","str"),
            ],
        },

        { # Responsabilita 
            "model_name":"Responsabilita",
            "model_obj":Responsabilita,
            "field_list":[
                ("responsabilita","str"),
            ],
        }, 
    ]

dump_dict = {}

for m_dict in model_dicts:
    populate_model_dict(m_dict)
    print("----------------------------FINITO MODELLO",m_dict)
    raw_input()
