# -*- coding: utf-8 -*-

#! /usr/bin/pythonimport json
# exec(open("/home/ema/projects/LiderLab/odp/ODP/db_stuff/db_update.py","r").read())
from odp_app.models import *
from django.db import transaction
from datetime import date
import json,os,re
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
debug_flag = True


MEDIA_BACKUP_PATH = "/home/ema/projects/LiderLab/odp/ODP/db_stuff/copia_media/media/copia-media"
DB_STUFF_PATH = "/home/ema/projects/LiderLab/odp/ODP/db_stuff"
def save_fileField(fieldname,jsonval,model_inst):
    # jsonval is the old path -> get the newname
    if jsonval == None:
        return None
    file_relpath = jsonval.split("/var/lib/django-media/")[1]
    file_name = re.split("immagine/|commento/|scheda/|sir_tiff/",file_relpath)[-1]
    # try to find the file, if it exists
    try:
        f = open(os.path.join(MEDIA_BACKUP_PATH,file_relpath),"rb") #reading binary is vital!
    except:
        logfile.write("FILE NOT FOUND" + file_relpath+"\n")
        print("---------FILE NOT FOUND:"+file_relpath+"---------")
        input()
        return None

    ff = File(f)
    getattr(model_inst,fieldname).save(file_name,ff)
    # model_inst.save() NOOOOOOOO NOT HERE!!!!!
    return True

def save_ManyMany(fieldname,t,jsonval,model_name,model_inst):
    # shall save, not return
    if t == 'd': # direct many to many relationship 
        pointed_modelname = models_dict[model_name]["foreign_dict"][fieldname]
        pointed_model = models_dict[pointed_modelname]["model_obj"]
        print("manymany!","json:",jsonval,"modello:",pointed_model) # DEBUG
        pointed_list = [] # the list of objects due to this manymany relationship
        for old_pk in jsonval: # jsonval is the old pk's list
            assert(type(old_pk) is int)
            new_pk = pk_remap[pointed_modelname][int(old_pk)]# get the new pk of the associated model instance. old_pk è gia un int
            pointed_inst = pointed_model.objects.get(pk=new_pk)# get the object 
            pointed_list.append(pointed_inst)
        
        # now save the new queryset
        try:
            print(len(pointed_list),pointed_list)
        except:
            print("Something wrong - manymany")
        getattr(model_inst,fieldname).set(pointed_list)
        # model_inst.save() could be but not really
        return True

def field_value(fieldname,fieldtype, jsonval, model_name):
    # ^ second element in tuple 
    global debug_flag
    if jsonval == None: # if there none, blanks or so....
        return None
    
    if fieldtype == "int": 
        return int(jsonval) 
    if t == "dec":
        try:
            return Decimal(fieldval)
        except:
            assert(fieldval is None)
            return None
    if fieldtype == "str": 
        return jsonval # may be ''
    if fieldtype == "date": #like YYYYMMGG     
        return date(int(jsonval[0:4]),int(jsonval[4:6]),int(jsonval[6:8]))

    if fieldtype == "foreignkey":
        pointed_modelname = models_dict[model_name]["foreign_dict"][fieldname]
        pointed_model = models_dict[pointed_modelname]["model_obj"]
        pointed_pk = pk_remap[pointed_modelname][int(jsonval)] #jsonval is the old pk that is pointed to!
        return pointed_model.objects.get(pk=pointed_pk) # the foreignkey is the obj
    
    if fieldtype == "bool":
        return jsonval

@transaction.atomic
def save_row(row_json_dict, model_obj,model_name):
    # saves a SINGLE INSTANCE of a model, given the dict with its attributes
    # is like {"field1":value1,"filed2",field}
    i = model_obj()
    if debug_flag:
        print("chiavi dict:",row_json_dict.keys())
    
    for fieldname, fieldtype in models_dict[model_name]["fields_dict"].items():
        jsonval = row_json_dict[fieldname] # get the json-field relative value
        if fieldname != "ocr": #debug_flag: #and 
            print("salvo field",fieldname,jsonval)
        else:
            print("ocr, len",len(jsonval))
        # get the field type
        fieldtype = models_dict[model_name]["fields_dict"][fieldname]
        if fieldtype == "file":
            assert(False)
        # elif fieldtype == "other":
        else:
            fieldval = field_value(fieldname,fieldtype, jsonval, model_name)
            setattr(i,fieldname,fieldval)

        if debug_flag and fieldname != "old_pk":
            try:
                if fieldname != "ocr":
                    print("field",fieldname,getattr(i,fieldname),"\n")
                else:
                    print("ocr done")
            except:
                print("getattr fails: writerule returned",fieldval)
    i.save() # save the model
    try:
        print("Saved normal fields",i)
    except:
        print("cannot print obj,saving it")
    # save the pk remappings
    pk_remap[model_name].update({row_json_dict["old_pk"]:i.pk})

    # after creating the object in the db, save the many to many relationships
    if "many_to_many_dict" in models_dict[model_name].keys():
        for fieldname, fieldtype in models_dict[model_name]["many_to_many_dict"].items():
            jsonval = row_json_dict[fieldname] # get the json-field relative value
            assert(
                save_ManyMany(
                    fieldname=fieldname,
                    t=fieldtype[-1],
                    jsonval=jsonval,
                    model_name=model_name,
                    model_inst=i
                    )
            )
            if debug_flag:
                try:
                    print("manymany:",fieldname,"value:",getattr(i,fieldname).all(),"jsonval:",jsonval)
                except:
                    print("problems printing",fieldname)
                    print(type(getattr(i,fieldname)))
        i.save() # save the many to many added relationships
    if "files_list" in models_dict[model_name].keys():
        for fieldname in models_dict[model_name]["files_list"]:
            jsonval = row_json_dict[fieldname] # get the json-field relative value
            retval = save_fileField(fieldname=fieldname,jsonval=jsonval,model_inst=i) # fieldval is taken just as backup
            if debug_flag:
                try:
                    print("Filefield:",fieldname,"value:",getattr(i,fieldname),"jsonval:",jsonval,"retval:",retval)
                    if retval is None and jsonval is not None:
                        print("Unexpected behaviour")
                except:
                    print("problems printing",fieldname)
                    print(type(getattr(i,fieldname)))
        i.save()

    print("Finished saving instance",i)

    return i.pk

def save_model(instances_list, model_obj, model_name):
    # saves an entire table
    print("beginning to save",model_obj,model_name)
    input("continue")
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


def save_group(ng):
    # open the relative file
    json_rel_path = "gruppo"+str(ng)+".json"
    f = open(os.path.join(DB_STUFF_PATH,json_rel_path),"r")
    db_dict = json.load(f)
    #get the function to call
    handle_dict = {
        1:group1,
        2:group2,
        3:group3,
    }
    handle = handle_dict[ng]
    models_list = handle() # get modellist
    # save each model in model list (in the group)
    for (modelname,) in models_list:
        save_model(
                instances_list=db_dict[modelname],
                model_obj=models_dict[model_name]["model_obj"]],
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
        # json keys are unicode, json values are number (if it's the case)
        pk_remap[m_name].update({int(k):v for k,v in m_remap_dict.items()})
    print("successfully created pk_remap")

except IOError:
    print("File con le pk non trovato!")
    pk_remap = {}

logfile_rel_path = "errori.log"
logfile = open(os.path.join(DB_STUFF_PATH,logfile_rel_path),"w")

exec(open(os.path.join(DB_STUFF_PATH,"models_dict.py"),"r").read())