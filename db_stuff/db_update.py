# -*- coding: utf-8 -*-

#! /usr/bin/pythonimport json
from odp_app.models import *
from django.db import transaction

"""struttura: {
 name --> nome del modello
    "name":[ # (names of models are unique)
                { # each dict is an instance of the model
                    - as many key:value as the model coloumns  
                        <filed name>:str or json serializabile
                    - and a key, value pair like
                        "old_pk": int, the old pk
                }, # each dict is an instance of the model
    ] # each model a list of instances
 }"""


models_dict = {
        "Regione":{
            "model_obj":Regione,
            "field_list":[
                ("regione","str"),
            ],
        }, 

        "Provincia":{
            "model_obj":Provincia,
            "field_list":[
                ("regione","foreignkey"),
                ("provincia","str"),
                ("targa","str"),
            ],
        },

        "Comune":{
            "model_obj":Comune,
            "field_list":[
                ("provincia","foreignkey"),
                ("comune","str"),
                ("codice","str"),
            ],
        },

        "Esaminatore":{
            "model_obj":Esaminatore,
            "field_list":[
                ("esaminatore","str"),
            ],
        },
        "Osservatorio":{
            "model_obj":Osservatorio,
            "field_list":[
                ("osservatorio","str"),
            ],
        },

        "Assicurazione":{
            "model_obj":Assicurazione,
            "field_list":[
                ("assicurazione","str"),
            ],
        },

        "Provenienza":{
            "model_obj":Provenienza,
            "field_list":[
                ("provenienza","str"),
            ],
        },

        "Responsabilita":{
            "model_obj":Responsabilita,
            "field_list":[
                ("responsabilita","str"),
            ],
        }, 
}
def field_value(jsonval,model_name):
    t = model_dicts[]

@transaction.atomic
def save_row(row_dict, model_obj,model_name):
    # saves a SINGLE INSTANCE of a model, given the dict with its attributes
    # is like {"field1":value1,"filed2",field}
    i = model_obj()
    for fieldname, jsonval in row_dict.items():# sett all the attributes apart old_pk
        fieldval = field_value(jsonval,model_name)
        if fieldname != "old_pk":
            setattr(i,fieldname,fieldval)
    # save the pk remappings 
    i.save()
    pk_remap_dict[model_name].update{row_dict[old_pk]:i.pk}
    return i.pk

def save_model(instances_list, model_obj, model_name):
    # saves an entire table
    for row_dict in instances_list:
        idx = save_row(row_dict, model_obj, model_name)
    
    print("Saved table: ",model_name, "last pk:",idx)

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

def save_group()

models_list = []
