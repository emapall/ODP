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
                "provincia":"str",
                "targa":"str",
            },
            "foreign_dict":{ # the dict containing the foreing keys and manytomany associations
                "regione":"Regione",                
            },
        },
        "Comune":{
            "model_obj":Comune,
            "fields_dict":{
                "provincia":"foreignkey",
                "comune":"str",
                "codice":"str",
            },
            "foreign_dict":{ # the dict containing the foreing keys and manytomany associations
                "provincia":"Provincia",                
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
                "responsabilita":"foreignkey",
                "sede_tribunale":"foreignkey",
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
            "foreign_dict":{ # the dict containing the foreing keys and manytomany associations
                "provenienza":"Provenienza",
                "responsabilita":"Responsabilita",
                "sede_tribunale":"Comune",
                "esaminatore":"Esaminatore",
                "osservatorio":"Osservatorio",
                "assicurazione":"Assicurazione",
                                
            },
            "many_to_many_dict":{
                "esaminatore":"manytomany-d",
                "osservatorio":"manytomany-d",
                "assicurazione":"manytomany-d",
            },
            "files_list":["file_cmn","file_img","file_sch"],
        },
        "Lesione":{
            "model_obj":Lesione,
            "fields_dict":{
                "lesione":"str",
            },
        },
        "Postumo":{
            "model_obj":Postumo,
            "fields_dict":{
                "postumo":"str",
            },
        },
        "Postumo_tabulato":{
            "model_obj":Postumo_tabulato,
            "fields_dict":{
                "postumo_tabulato":"str",
            },
        },
        "RichiestaParteAttrice":{
            "model_obj":RichiestaParteAttrice,
            "fields_dict":{
                "richiesta":"str",
            },
        },
        "DannoPatrimoniale":{
            "model_obj":DannoPatrimoniale,
            "fields_dict":{
                "tipo":"str",
            },
        },
        "DirittoInviolabile":{
            "model_obj":DirittoInviolabile,
            "fields_dict":{
                "diritto":"str",
            },
        },
        "Professione":{
            "model_obj":Professione,
            "fields_dict":{
                "professione":"str",
            },
        },
        "FattoreLiquidazione":{
            "model_obj":FattoreLiquidazione,
            "fields_dict":{
                "fattore":"str",
            },
        },
        "FattoreLiquidazioneDP":{
            "model_obj":FattoreLiquidazioneDP,
            "fields_dict":{
                "fattore":"str",
            },
        },
        "ProvaDelDNP":{
            "model_obj":ProvaDelDNP,
            "fields_dict":{
                "prova":"str",
            },
        },
        "ProvaDelDP":{
            "model_obj":ProvaDelDP,
            "fields_dict":{
                "prova":"str",
            },
        },
        "TrendLiquidazione":{
            "model_obj":TrendLiquidazione,
            "fields_dict":{
                "trend":"str",
            },
        },
        "Infortunato":{
            "model_obj":Infortunato,
            "fields_dict":{
                "professione":"foreignkey",
                "sentenza":"foreignkey",
                "accoglimento_giudice":"str",
                "altri_danni":"str",
                "criterio_liquidazione":"str",
                "ctp_nominati":"str",
                "desc_rif_tabellare":"str",
                "dm_dbjh_est":"bool",
                "dm_dbjh_importo_liquidazione":"dec",
                "dm_est":"bool",
                "durata_dmit":"int",
                "ente_sociale":"str",
                "est_clg":"bool",
                "est_cls":"bool",
                "est_das_ip":"str",
                "est_das_it":"str",
                "est_dm":"bool",
                "est_dm_ip":"bool",
                "est_dm_it":"bool",
                "est_dm_vp":"bool",
                "est_interazione":"bool",
                "est_ip":"bool",
                "est_it":"bool",
                "est_lcip":"bool",
                "est_lcit":"bool",
                "est_maggiorenne":"str",
                "est_pddb":"bool",
                "est_rdjh":"bool",
                "est_ss":"bool",
                "est_ss_future":"bool",
                "est_ss_sostenute":"bool",
                "eta":"int",
                "euro_al_di":"dec",
                "flag_rif_tabellare":"bool",
                "flag_vis_spec":"str",
                "giorni_lcit":"int",
                "importo_ad":"dec",
                "importo_altri_danni":"dec",
                "importo_danni_cose":"dec",
                "importo_dannopatrimoniale":"dec",
                "importo_dap":"dec",
                "importo_dirittoinviolabile":"dec",
                "importo_future":"dec",
                "importo_liquidato":"dec",
                "importo_liquidazione_das":"dec",
                "importo_liquidazione_das_ip":"dec",
                "importo_liquidazione_das_it":"dec",
                "importo_liquidazione_dm":"dec",
                "importo_liquidazione_dmip":"dec",
                "importo_liquidazione_dmit":"dec",
                "importo_liquidazione_lcip":"dec",
                "importo_liquidazione_lcit":"dec",
                "importo_provvisionale":"dec",
                "importo_rivalutazione":"dec",
                "importo_sostenute":"dec",
                "importo_sr":"dec",
                "importo_totale":"dec",
                "interessi_dannopatrimoniale":"date",
                "interessi_dirittoinviolabile":"date",
                "interessi_legali_dc":"date",
                "interessi_legali_dm":"date",
                "interessi_legali_ip":"date",
                "interessi_legali_it":"date",
                "interessi_legali_lcip":"date",
                "interessi_legali_lcit":"date",
                "interessi_legali_ss":"date",
                "liquidazione_totale":"dec",
                "metodo_das_ip":"str",
                "metodo_das_it":"str",
                "metodo_di_quantificazione":"str",
                "metodo_lcip":"str",
                "metodo_lcit":"str",
                "motivazione":"str",
                "note_ctu":"str",
                "note_dannopatrimoniale":"str",
                "note_dirittoinviolabile":"str",
                "note_dm":"str",
                "note_exaltrespese":"str",
                "note_fattori_rilevanti_liquidazione":"str",
                "note_fattori_rilevanti_liquidazione_dp":"str",
                "note_gen":"str",
                "note_generale":"str",
                "note_importi":"str",
                "note_ip":"str",
                "note_it":"str",
                "note_prova_del_dnp":"str",
                "note_prova_del_dp":"str",
                "note_trend_liquidazione":"str",
                "percentuale_colpa_attore":"dec",
                "percentuale_das_ip":"dec",
                "percentuale_dmip":"dec",
                "percentuale_lcip":"dec",
                "percentuale_pddb":"dec",
                "periodo_di_sopravvivenza":"str",
                "pre2001":"bool",
                "pubblicabile":"bool",
                "qualifica_ctu":"str",
                "resoconto_op_per":"str",
                "sede_tabella":"str",
                "sesso":"str",
                "sunt_diritti_lesi":"bool",
                "tabella":"bool",
                "tipo_ana_generale":"str",
                "tipo_ana_lavorativa":"str",
                "tipo_ctp":"str",
                "tipo_ctu":"str",
                "tipo_doc_medica":"str",
                "tipo_eo_generale":"str",
                "tipo_eo_specifico":"str",
                "tipo_esami_strumentali":"str",
                "tipo_fatto_mod":"bool",
                "tipo_fatto_primer":"bool",
                "tipo_fatto_ritorno":"bool",
                "tipo_fatto_solltra":"bool",
                "tipo_lesione":"str",
                "tipo_quesito":"str",
                "tipo_quesito_clg":"bool",
                "tipo_quesito_cls":"bool",
                "tipo_quesito_db":"bool",
                "tipo_quesito_de":"bool",
                "tipo_quesito_ndc":"bool",
                "tipo_quesito_sa":"bool",
                "tipo_quesito_sf":"bool",
                "tipo_quesito_ss":"bool",
                "tipo_quesito_t":"bool",
                "tipo_risposta_quesiti":"str",
                "tipo_rivalutazione":"str",
                "tipo_sr":"str",
                "tipo_stato_attuale":"str",
                "tipo_trat_ml":"str",
            },
            "foreign_dict":{ # the dict containing the foreing keys and manytomany associations
                "professione":"Professione",
                "sentenza":"Sentenza",
                "lesione":"Lesione",                                
                "postumo":"Postumo",                                
                "postumo_tabulato":"Postumo_tabulato",                                
                "richiestaparteattrice":"RichiestaParteAttrice",                                
                "dannopatrimoniale":"DannoPatrimoniale",                                
                "dirittoinviolabile":"DirittoInviolabile",                                
                "fattori_rilevanti_liquidazione":"FattoreLiquidazione",                                
                "fattori_rilevanti_liquidazione_dp":"FattoreLiquidazioneDP",
                "prova_del_dnp":"ProvaDelDNP",                                
                "prova_del_dp":"ProvaDelDP",                                
                "trend_liquidazione":"TrendLiquidazione",                                                         
            },
            "many_to_many_dict":{
                "lesione":"manytomany-d",
                "postumo":"manytomany-d",
                "postumo_tabulato":"manytomany-d",
                "richiestaparteattrice":"manytomany-d",
                "dannopatrimoniale":"manytomany-d",
                "dirittoinviolabile":"manytomany-d",
                "fattori_rilevanti_liquidazione":"manytomany-d",
                "fattori_rilevanti_liquidazione_dp":"manytomany-d",
                "prova_del_dnp":"manytomany-d",
                "prova_del_dp":"manytomany-d",
                "trend_liquidazione":"manytomany-d",
            },
        },

        "Invalidita_temporanea":{
            "model_obj":Invalidita_temporanea,
            "fields_dict":{
                "infortunato":"foreignkey",
                "giorni":"int",
                "percentuale":"dec",
            },
            "foreign_dict":{ # the dict containing the foreing keys and manytomany associations
                "infortunato":"Infortunato",                              
            },
        },
        
        "TrendProfiloRilevanteContainer":{
            "model_obj":TrendProfiloRilevanteContainer,
            "fields_dict":{
                "sentenza":"foreignkey",
                "trend":"foreignkey",
            },
            "foreign_dict":{ # the dict containing the foreing keys and manytomany associations
                "sentenza":"Sentenza",    
                "trend":"TrendProfiloRilevante", 
                "profili_rilevanti":"ProfiloRilevante",                         
            },
            "many_to_many_dict":{
                "profili_rilevanti":"manytomany-d",
            }
        },

        "ProfiloRilevante":{
            "model_obj":ProfiloRilevante,
            "fields_dict":{
                "trend":"foreignkey",
                "profilo":"str",
            },
            "foreign_dict":{ # the dict containing the foreing keys and manytomany associations
                "trend":"TrendProfiloRilevante", 
            },
        },

        "TrendProfiloRilevante":{
            "model_obj":TrendProfiloRilevante,
            "fields_dict":{
                "trend":"str",
            },

        },


}