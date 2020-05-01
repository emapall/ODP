# -*- coding: utf-8 -*-

#! /usr/bin/pythonimport json
from odp_app.models import *
from django.db import transaction
from datetime import date
import json,os
from django.core.files import File

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

MEDIA_BACKUP_PATH = "/home/ema/projects/LiderLab/odp/ODP/db_stuff/copia_media/media/copia-media"

@transaction.atomic
def save_fileField(fieldname,jsonval,model_obj):
    # jsonval is the old path -> get the newname
    file_name = jsonval.split("/var/lib/django-media/")[1]
    f = open(os.path.join(MEDIA_BACKUP_PATH,file_name),"rb")
    ff = File(f)
    getattr(model_obj,fieldname).save(file_name,ff)
    model_obj.save()
    return True

def field_value(fieldname,fieldtype, jsonval, model_name):
    # ^ second element in tuple 
    if jsonval == None: # if there none, blanks or so....
        return None
    
    if fieldtype == "int": 
        return int(jsonval) 
    if fieldtype == "str": 
        return jsonval # may be ''
    if fieldtype == "date": #like YYYYMMGG
        return date(int(jsonval[0:4]),int(jsonval[4:6]),int(jsonval[6:8]))

    if fieldtype == "foreignkey":
        pointed_modelname = models_dict[model_name]["fields_dict"][str(fieldname+"_name")]
        pointed_model = models_dict[pointed_modelname]["model_obj"]
        pointed_pk = pk_remap[pointed_modelname][int(jsonval)] #jsonval is the old pk that is pointed to!
        return pointed_model.objects.get(pk=pointed_pk) # the foreignkey stores the obj, not the pk
    if fieldtype == "bool":
        return jsonval # may NOT be none


@transaction.atomic
def save_row(row_dict, model_obj,model_name):
    # saves a SINGLE INSTANCE of a model, given the dict with its attributes
    # is like {"field1":value1,"filed2",field}
    i = model_obj()
    for fieldname, jsonval in row_dict.items():# sett all the attributes apart old_pk
        if fieldname != "old_pk":
            fieldtype = models_dict[model_name]["fields_dict"][fieldname]
            if fieldtype == "file":
                assert(False)
            #elif altra robba
            else:
                fieldval = field_value(fieldname,fieldtype, jsonval, model_name)
                setattr(i,fieldname,fieldval)
    # save the pk remappings
    print("Sto per salvare",i)
    i.save()
    pk_remap[model_name].update({row_dict["old_pk"]:i.pk})
    return i.pk

def save_model(instances_list, model_obj, model_name):
    # saves an entire table
    print("inizio a salvare",model_obj,model_name)
    input("Continuare")
    input("segur")
    pk_remap.update({model_name:{}})
    n = 0
    for row_dict in instances_list:
        idx = save_row(row_dict, model_obj, model_name)
        n += 1
    
    print("Saved table: ",model_name, "last pk:",idx, "n:",n)
    input("Continuare")
    input("segur")


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

def save_group(ng):
    
    f = open("db_stuff/gruppo"+str(ng)+".json","r")
    db_dict = json.load(f)
    handle_dict = {
        1:group1,
        2:group2,
    }
    handle = handle_dict[ng]
    models_list = handle()
    for (modelname,modelobj) in models_list:
        
        save_model(
                instances_list=db_dict[modelname],
                model_obj=modelobj,
                model_name=modelname,
                )
    f = open("db_stuff/pk_remap.json","w")
    json.dump(pk_remap,f)

models_list = []
try:    
    pk_file = open("db_stuff/pk_remap.json","r")
    pk_remap_json = json.load(pk_file) # Le chiavi sono str!
    pk_remap = {}
    for m_name, m_remap_dict in pk_remap_json.items():
        print("creo remap per modello",m_name,m_remap_dict)
        pk_remap.update({m_name:{}})
        pk_remap[m_name].update({int(k):v for k,v in m_remap_dict.items()})
except IOError:
    print("File con le pk non trovato!")
    pk_remap = {}



models_dict = {
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
                "regione_name":"Regione",
                "provincia":"str",
                "targa":"str",
            },
        },
        "Comune":{
            "model_obj":Comune,
            "fields_dict":{
                "provincia":"foreignkey",
                "provincia_name":"Provincia",
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
                "provenienza_name":"Provenienza",
                "responsabilita":"foreignkey",
                "responsabilita_name":"Responsabilita",
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