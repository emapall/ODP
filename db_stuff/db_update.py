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

global debug_flag 
debug_flag = False


MEDIA_BACKUP_PATH = "/home/ema/projects/LiderLab/odp/ODP/db_stuff/copia_media/media/copia-media"
DB_STUFF_PATH = "/home/ema/projects/LiderLab/odp/ODP/db_stuff"
@transaction.atomic
def save_fileField(fieldname,jsonval,model_inst):
    # jsonval is the old path -> get the newname
    if jsonval == None:
        return None
    file_name = jsonval.split("/var/lib/django-media/")[1]
    
    # try to find the file, if it exists
    try:
        f = open(os.path.join(MEDIA_BACKUP_PATH,file_name),"rb") #reading binary is vital!
    except:
        logfile.write("FILE NOT FOUND" + file_name+"\n")
        return None

    ff = File(f)
    getattr(model_inst,fieldname).save(file_name,ff)
    model_inst.save()
    return True

@transaction.atomic
def save_ManyMany(fieldname,t,jsonval,model_name,model_inst):
    # shall save, not return
    if t == "d": # direct many to many relationship 
        pointed_modelname = models_dict[model_name]["fields_dict"][str(fieldname+"_name")]
        pointed_model = models_dict[pointed_modelname]["model_obj"]

        pointed_list = [] # the list of objects due to this manymany relationship
        for old_pk in jsonval: # jsonval is the old pk's list
            assert(type(old_pk) is int)
            new_pk = pk_remap[pointed_modelname][int(old_pk)]# get the new pk of the associated model instance. old_pk è gia un int
            pointed_inst = pointed_model.objects.get(pk=new_pk)# get the object
            # 
            pointed_list.append(pointed_inst)
        
        # now save the new queryset
        getattr(model_inst,fieldname).set(pointed_list)
        model_inst.save()

        return True

def field_value(fieldname,fieldtype, jsonval, model_name):
    # ^ second element in tuple 
    global debug_flag
    if jsonval == None: # if there none, blanks or so....
        return None
    
    if fieldtype == "int": 
        return int(jsonval) 
    if fieldtype == "str": 
        return jsonval # may be ''
    if fieldtype == "date": #like YYYYMMGG
        if jsonval == "20011129":
            debug_flag = True
            print("ciaissimo!------------------",debug_flag)
            input()
            
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
    if debug_flag:
        print("chiavi dict:",row_dict.keys())
    count = 0
    for fieldname, jsonval in row_dict.items():# sett all the attributes apart old_pk
        if debug_flag: #and fieldname != "ocr":
            print("salvo field",count,"-",len(row_dict.keys()),fieldname,jsonval)
            count += 1
            input()
        if fieldname != "old_pk":
            fieldtype = models_dict[model_name]["fields_dict"][fieldname]
            if fieldtype == "file":
                fieldval = save_fileField(fieldname=fieldname,jsonval=jsonval,model_inst=i)
            elif fieldtype == "manytomany-d":
                fieldval = save_ManyMany(fieldname=fieldname,t=fieldtype,jsonval=jsonval,model_name=model_name,model_inst=i)
            else:
                fieldval = field_value(fieldname,fieldtype, jsonval, model_name)
                setattr(i,fieldname,fieldval)
        if debug_flag and fieldname != "old_pk" and "name" not in fieldname:
            try:
                print("fatto field",count,"-",len(row_dict.keys()),fieldname,getattr(i,fieldname),"\n")
            except:
                print("getattr fails: writerule returned",fieldval)

    # save the pk remappings
    try:
        print("Sto per salvare",i)
    except:
        pass
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
    # open the relative file
    json_rel_path = "gruppo"+str(ng)+".json"
    f = open(os.path.join(DB_STUFF_PATH,json_rel_path),"r")
    db_dict = json.load(f)
    #get the function to call
    handle_dict = {
        1:group1,
        2:group2,
    }
    handle = handle_dict[ng]
    models_list = handle() # get modellist
    # save each model in model list (in the group)
    for (modelname,modelobj) in models_list:
        save_model(
                instances_list=db_dict[modelname],
                model_obj=modelobj,
                model_name=modelname,
                )
    pk_rel_path = "pk_remap.json"
    pk_file = open(os.path.join(DB_STUFF_PATH,pk_rel_path),"w")
    json.dump(pk_remap,pk_file)
    pk_file.close()
    logfile.close()


models_list = []
try: 
    # read pks  
    pk_rel_path = "pk_remap.json" 
    pk_file = open(os.path.join(DB_STUFF_PATH,pk_rel_path),"r")
    pk_remap_json = json.load(pk_file) # Le chiavi sono str!
    pk_remap = {}
    # create the pk remap dict
    for m_name, m_remap_dict in pk_remap_json.items():
        pk_remap.update({m_name:{}})
        pk_remap[m_name].update({int(k):v for k,v in m_remap_dict.items()})
    print("successfully created pk_remap")

except IOError:
    print("File con le pk non trovato!")
    pk_remap = {}

logfile_rel_path = "errori.log"
logfile = open(os.path.join(DB_STUFF_PATH,logfile_rel_path),"w")


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
                "provenienza_name":"Provenienza",
                "responsabilita":"foreignkey",
                "responsabilita_name":"Responsabilita",
                "sede_tribunale":"foreignkey",
                "sede_tribunale_name":"Comune",
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
                "esaminatore":"manytomany-d",
                "esaminatore_name":"Esaminatore",
                "osservatorio":"manytomany-d",
                "osservatorio_name":"Osservatorio",
                "assicurazione":"manytomany-d",
                "assicurazione_name":"Assicurazione",
            },
        },
}
