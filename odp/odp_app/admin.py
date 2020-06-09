# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from odp_app.models import (
    Assicurazione,
    Comune,
    DannoPatrimoniale,
    DirittoInviolabile,
    Esaminatore,
    FattoreLiquidazione,
    FattoreLiquidazioneDP,
    Infortunato,
    Invalidita_temporanea,
    Lesione,
    Osservatorio,
    Postumo,
    Postumo_tabulato,
    Professione,
    ProfiloRilevante,
    ProvaDelDNP,
    ProvaDelDP,
    Provenienza,
    Provincia,
    Regione,
    Responsabilita,
    RichiestaParteAttrice,
    Sentenza,
    TrendLiquidazione,
    TrendProfiloRilevante,
    TrendProfiloRilevanteContainer,
    User,
)

# from lider.odp.widgets import *


class ComuneAdmin(admin.ModelAdmin):
    search_fields = ["comune", "codice"]


class ProfessioneAdmin(admin.ModelAdmin):
    search_fields = ["professione"]


class LesioneAdmin(admin.ModelAdmin):
    search_fields = ["id", "lesione"]
    list_display = ["id", "lesione"]


class PostumoAdmin(admin.ModelAdmin):
    search_fields = ["id", "postumo"]
    list_display = ["id", "postumo"]


class AssicurazioneAdmin(admin.ModelAdmin):
    search_fields = ["id", "assicurazione"]
    list_display = ["id", "assicurazione"]


class PostumoTabulatoAdmin(admin.ModelAdmin):
    search_fields = ["id", "postumo_tabulato"]
    list_display = ["id", "postumo_tabulato"]


class InvaliditaTemporaneaInline(admin.TabularInline):
    #    extra = 4
    model = Invalidita_temporanea


class ProfiloRilevanteInline(admin.StackedInline):
    extra = 1

    # TODO implement widgets

    # formfield_overrides = {
    # models.ForeignKey: {"widget": TrendWidget},
    #             models.ManyToManyField: {'widget' : ProfiloWidget},
    # }
    model = TrendProfiloRilevanteContainer


class SentenzaAdmin(admin.ModelAdmin):
    inlines = [ProfiloRilevanteInline]
    fieldsets = (
        ("Stato rilettura", {"fields": ("forza_esclusione",)}),
        (None, {"fields": ("esaminatore", "osservatorio")}),
        (
            "Dati sentenza",
            {
                "fields": (
                    ("anno_di_arrivo", "numero_della_sentenza", "estctu"),
                    ("provenienza", "codice", "estensore"),
                    ("grado_di_giudizio", "sede_tribunale", "numero_della_sezione"),
                    ("data_della_citazione", "data_della_sentenza"),
                    ("data_del_deposito", "anno_del_deposito"),
                    ("data_del_fatto", "fatto"),
                    ("numero_attori", "numero_convenuti", "numero_terzi"),
                    ("responsabilita", "riconvenzionale"),
                    ("assicurazione",),
                )
            },
        ),
        ("Note", {"classes": ["collapse"], "fields": ("note_sentenza",)}),
        ("Materiale extra", {"classes": ["collapse"], "fields": ("ocr", "file_img")}),
        (None, {"fields": (("note_profili_rilevanti"),)}),
    )
    filter_horizontal = ("esaminatore",)
    list_display = (
        "id",
        "forza_esclusione",
        "codice",
        "grado_di_giudizio",
        "sede_tribunale",
        "data_della_sentenza",
        "data_della_citazione",
        "data_del_fatto",
        "files_allegati",
    )
    list_display_links = (
        "id",
        "sede_tribunale",
        "data_della_sentenza",
        "data_della_citazione",
        "data_del_fatto",
    )
    raw_id_fields = ("sede_tribunale", "assicurazione")
    search_fields = ["id", "codice", "grado_di_giudizio", "sede_tribunale__comune"]
    save_on_top = True


#    fields = (
#        ('Informazioni generali', {
#            'fields': ('grado_di_giudizio', 'sede_tribunale', 'data_della_sentenza', 'numero_della_sentenza', 'estensore', 'osservatorio')
#        }),
#        ('Dati di revisione<!--perms ="1"   -->', {
#            'fields': ('esaminatore', 'data_del_deposito')
#        }),
#    )
#    list_filter = ['data_della_sentenza']
#    search_fields = ['sede_tribunale', 'data_del_fatto', 'data_della_citazione', 'data_della_sentenza', 'file_img', 'file_sch', 'file_cmn',]


class DanneggiatoForm(forms.ModelForm):
    class Meta:
        model = Infortunato
        # TODO list only interesting fields
        fields = "__all__"

    def clean(self):
        cleaned_data = self.cleaned_data

        #    metodo_das_it            DipendeDa_est_it
        #    est_lcit            DipendeDa_est_it
        #    metodo_lcit            DipendeDa_est_it
        #    importo_liquidazione_lcit    DipendeDa_est_it
        #    giorni_lcit            DipendeDa_est_it
        #    interessi_legali_it        DipendeDa_est_it
        #
        #    interessi_legali_lcip        DipendeDa_est_ip
        #    metodo_das_ip            DipendeDa_est_ip
        #    percentuale_das_ip        DipendeDa_est_ip
        #    importo_liquidazione_das_ip    DipendeDa_est_ip
        #    est_lcip            DipendeDa_est_ip
        #    metodo_lcip            DipendeDa_est_ip
        #    percentuale_lcip        DipendeDa_est_ip
        #    importo_liquidazione_lcip    DipendeDa_est_ip
        #    interessi_legali_ip        DipendeDa_est_ip
        #
        #    interessi_legali_lcit        DipendeDa_est_lcit
        #
        #    motivazione            DipendeDa_est_dm
        #    interessi_legali_dm        DipendeDa_est_dm
        #
        #    importo_liquidazione_dmip    DipendeDa_est_dmip
        #    percentuale_dmip        DipendeDa_est_dmip
        #
        #    importo_liquidazione_dmit    DipendeDa_est_dmit
        #    durata_dmit            DipendeDa_est_dmit
        #
        #    interessi_legali_ss        DipendeDa_est_ss

        # CampiControllo = [
        #    "est_it",
        #    "est_ip",
        #    "est_lcit",
        #    "est_dm",
        #    "est_dmip",
        #    "est_dmit",
        #    "est_ss",
        # ]

        DipendeDa = {
            "est_it": [
                "metodo_das_it",
                "euro_al_di",
                "importo_liquidazione_das_it",
                "interessi_legali_it",
                "est_lcit",
                "note_it",
            ],
            "est_lcit": [
                "giorni_lcit",
                "metodo_lcit",
                "importo_liquidazione_lcit",
                "interessi_legali_lcit",
            ],
            "est_ip": [
                "percentuale_das_ip",
                "metodo_das_ip",
                "tabella",
                "sede_tabella",
                "importo_liquidazione_das_ip",
                "interessi_legali_ip",
                "est_lcip",
                "note_ip",
            ],
            "est_lcip": [
                "metodo_lcip",
                "percentuale_lcip",
                "importo_liquidazione_lcip",
                "interessi_legali_lcip",
                "est_clg",
                "est_cls",
            ],
            "dm_est": ["dm_dbjh_est", "est_de", "note_morte"],
            "dm_dbjh_est": ["dm_dbjh_importo_liquidazione"],
            "est_de": ["importo_liquidazione_de", "interessi_legali_de"],
            "est_dm": [
                "motivazione",
                "est_dm_vp",
                "est_dm_it",
                "est_dm_ip",
                "note_dm",
                "interessi_legali_dm",
            ],
            "est_dm_vp": ["importo_liquidazione_dm"],
            "est_dm_it": ["durata_dmit", "importo_liquidazione_dmit"],
            "est_dm_ip": ["percentuale_dmip", "importo_liquidazione_dmip"],
            "est_ss": ["est_ss_sostenute", "est_ss_future"],
            "est_ss_sostenute": ["importo_sostenute", "interessi_legali_ss"],
            "est_ss_future": ["importo_future"],
            "importo_danni_cose": ["interessi_legali_dc"],
            "importo_altri_danni": ["altri_danni"],
            "importo_dannopatrimoniale": ["interessi_dannopatrimoniale"],
            "importo_dirittoinviolabile": ["interessi_dirittoinviolabile"],
        }

        msg = {
            "est_it": u"Il danneggiato non ha invalidità temporanea.",
            "est_lcit": u"Il danneggiato non ha lucro cessante per invalidità temporanea.",
            "est_ip": u"Il danneggiato non ha invalidità permanente.",
            "est_lcip": u"Il danneggiato non ha lucro cessante per invalidità permanente.",
            "dm_est": u"Il danneggiato non ha danno da morte.",
            "dm_dbjh_est": u"Il danneggiato non ha danno biologico jure ereditario.",
            "est_de": u"Il danneggiato non ha danno non patrimoniale da perdita del congiunto.",
            "est_dm": u"Il danneggiato non ha danno morale.",
            "est_dm_vp": u"Il danneggiato non ha danni morali in via equitativa pura.",
            "est_dm_it": u"Il danneggiato non ha danni morali da invalidità temporanea.",
            "est_dm_ip": u"Il danneggiato non ha danni morali da invalidità permanente.",
            "est_ss": u"Il danneggiato non ha risarcimento spese.",
            "est_ss_sostenute": u"Il danneggiato non ha risarcimento spese già sostenute.",
            "est_ss_future": u"Il danneggiato non ha risarcimento spese future.",
            "importo_danni_cose": u"Inserisci anche un importo dei danni alle cose.",
            "importo_altri_danni": u"Inserisci anche un importo degli altri danni.",
            "importo_dannopatrimoniale": u"Inserisci anche un importo per il danno patrimoniale",
            "importo_dirittoinviolabile": u"Inserisci anche un importo per il dnp da lesione di diritti inviolabili",
        }

        for controllo, dipendenze in DipendeDa.items():
            if not cleaned_data.get(controllo):
                for campo in dipendenze:
                    if cleaned_data.get(campo):
                        # TODO controllare
                        self._errors[campo] = forms.utils.ErrorList([msg[controllo]])
                        del cleaned_data[campo]

        return cleaned_data


class DanneggiatoAdmin(admin.ModelAdmin):
    form = DanneggiatoForm
    inlines = [InvaliditaTemporaneaInline]
    fieldsets = (
        # TODO: Trovare un modo migliore di fare l'associazione
        (None, {"fields": ("sentenza",)}),
        ("Stato rilettura", {"fields": ("pubblicabile",)}),
        (
            "Dati danneggiato",
            {
                "classes": ["collapse"],
                "fields": (
                    ("eta", "est_maggiorenne"),
                    ("sesso", "professione"),
                    ("note_gen",),
                ),
            },
        ),
        (
            "Generale",
            {
                "classes": ["collapse"],
                "fields": (
                    ("percentuale_colpa_attore",),
                    ("tipo_sr", "ente_sociale", "importo_sr"),
                    ("richiestaparteattrice",),
                    (
                        "fattori_rilevanti_liquidazione",
                        "note_fattori_rilevanti_liquidazione",
                    ),
                    ("prova_del_dnp", "note_prova_del_dnp"),
                    (
                        "fattori_rilevanti_liquidazione_dp",
                        "note_fattori_rilevanti_liquidazione_dp",
                    ),
                    ("prova_del_dp", "note_prova_del_dp"),
                    (
                        "trend_liquidazione",
                        "est_rdjh",
                        "est_interazione",
                        "note_trend_liquidazione",
                        "est_pddb",
                        "percentuale_pddb",
                    ),
                ),
            },
        ),
        (
            "Invalidità temporanea",
            {
                "classes": ["collapse"],
                "fields": (
                    ("est_it"),
                    ("metodo_das_it", "euro_al_di"),
                    ("importo_liquidazione_das_it", "interessi_legali_it"),
                    ("est_lcit", "giorni_lcit"),
                    ("metodo_lcit"),
                    ("importo_liquidazione_lcit", "interessi_legali_lcit"),
                    ("note_it"),
                ),
            },
        ),
        (
            "Invalidità permanente",
            {
                "classes": ["collapse"],
                "fields": (
                    ("est_ip"),
                    ("tipo_lesione",),
                    ("lesione",),
                    ("postumo_tabulato",),
                    ("postumo"),
                    ("percentuale_das_ip", "metodo_das_ip", "tabella", "sede_tabella"),
                    ("importo_liquidazione_das_ip", "interessi_legali_ip"),
                    ("est_lcip"),
                    ("metodo_lcip", "percentuale_lcip"),
                    ("importo_liquidazione_lcip", "interessi_legali_lcip"),
                    ("est_clg", "est_cls"),
                    ("note_ip"),
                ),
            },
        ),
        (
            "Danno non patrimoniale diverso dal danno alla salute",
            {
                "classes": ["collapse"],
                "fields": (
                    ("est_dm"),
                    ("motivazione", "interessi_legali_dm"),
                    ("est_dm_vp", "importo_liquidazione_dm"),
                    ("est_dm_it", "durata_dmit", "importo_liquidazione_dmit"),
                    ("est_dm_ip", "percentuale_dmip", "importo_liquidazione_dmip"),
                    ("note_dm"),
                    ("sunt_diritti_lesi"),
                    ("dirittoinviolabile"),
                    (
                        "importo_dirittoinviolabile",
                        "interessi_dirittoinviolabile",
                        "metodo_di_quantificazione",
                    ),
                    ("note_dirittoinviolabile"),
                ),
            },
        ),
        (
            "Danni da morte",
            {
                "classes": ["collapse"],
                "fields": (
                    ("dm_est"),
                    (
                        "dm_dbjh_est",
                        "dm_dbjh_importo_liquidazione",
                        "periodo_di_sopravvivenza",
                        "criterio_liquidazione",
                    ),
                    #    ('est_de', 'importo_liquidazione_de', 'interessi_legali_de'),
                    #    ('note_morte')
                ),
            },
        ),
        (
            "Danno patrimoniale - spese vive",
            {
                "classes": ["collapse"],
                "fields": (
                    ("est_ss"),
                    ("est_ss_sostenute", "importo_sostenute", "interessi_legali_ss"),
                    ("est_ss_future", "importo_future"),
                    ("importo_danni_cose", "interessi_legali_dc"),
                    ("note_exaltrespese"),
                    ("dannopatrimoniale"),
                    ("importo_dannopatrimoniale", "interessi_dannopatrimoniale"),
                    ("note_dannopatrimoniale"),
                ),
            },
        ),
        (
            "Generici altri danni",
            {
                "classes": ["collapse"],
                "fields": (("importo_altri_danni", "altri_danni"),),
            },
        ),
        ### Saranno popolati automaticamente
        #        ('Totale importi liquidati - provvisionale', {
        #            'classes': 'collapse',
        #            'fields': (
        #                ('importo_dap',),
        #                ('importo_ad',),
        #                ('importo_totale',),
        #                ('importo_provvisionale',),
        #                ('importo_liquidato',),
        #                ('tipo_rivalutazione','importo_rivalutazione'),
        #                ('liquidazione_totale',),
        #                ('note_importi',)
        #            )
        #        }),
        (
            "Totale importi liquidati - acconto",
            {
                "classes": ["collapse"],
                "fields": (
                    ("importo_provvisionale",),
                    ("tipo_rivalutazione", "importo_rivalutazione"),
                    ("note_importi",),
                ),
            },
        ),
        (
            "CTU",
            {
                "classes": ["collapse"],
                "fields": (
                    ("accoglimento_giudice", "tipo_ctu"),
                    ("tipo_quesito", "qualifica_ctu"),
                    ("tipo_ctp", "ctp_nominati"),
                    ("resoconto_op_per", "tipo_doc_medica"),
                    ("tipo_ana_generale", "tipo_ana_lavorativa"),
                    ("tipo_stato_attuale", "tipo_eo_generale"),
                    ("tipo_eo_specifico", "flag_vis_spec"),
                    ("tipo_esami_strumentali", "tipo_trat_ml"),
                    ("tipo_risposta_quesiti",),
                    ("tipo_quesito_ndc", "tipo_quesito_sa", "tipo_quesito_t"),
                    ("tipo_quesito_db", "tipo_quesito_clg", "tipo_quesito_cls"),
                    ("tipo_quesito_de", "tipo_quesito_ss", "tipo_quesito_sf"),
                    ("tipo_fatto_mod", "tipo_fatto_solltra"),
                    ("tipo_fatto_primer", "tipo_fatto_ritorno"),
                    ("flag_rif_tabellare",),
                    ("desc_rif_tabellare",),
                    ("note_ctu",),
                ),
            },
        ),
    )

    filter_horizontal = (
        "richiestaparteattrice",
        "dannopatrimoniale",
        "dirittoinviolabile",
        "fattori_rilevanti_liquidazione_dp",
        "fattori_rilevanti_liquidazione",
        "prova_del_dnp",
        "prova_del_dp",
        "trend_liquidazione",
    )
    save_on_top = True
    list_display = ("id", "professione", "sesso", "eta", "pubblicabile")
    raw_id_fields = ("sentenza", "lesione", "postumo", "postumo_tabulato")
    search_fields = ["id", "professione__professione", "eta"]
    list_display_links = ("id", "professione")


#    list_filter = ['pubblicabile']


admin.site.register(Esaminatore)
admin.site.register(Osservatorio)
admin.site.register(Assicurazione, AssicurazioneAdmin)
admin.site.register(Regione)
admin.site.register(Provincia)
admin.site.register(Comune, ComuneAdmin)
admin.site.register(Provenienza)
admin.site.register(Lesione, LesioneAdmin)
admin.site.register(Postumo, PostumoAdmin)
admin.site.register(Postumo_tabulato, PostumoTabulatoAdmin)
admin.site.register(RichiestaParteAttrice)
admin.site.register(DannoPatrimoniale)
admin.site.register(DirittoInviolabile)
admin.site.register(Professione, ProfessioneAdmin)
admin.site.register(Sentenza, SentenzaAdmin)
admin.site.register(Infortunato, DanneggiatoAdmin)
admin.site.register(Invalidita_temporanea)
admin.site.register(Responsabilita)
admin.site.register(FattoreLiquidazione)
admin.site.register(FattoreLiquidazioneDP)
admin.site.register(ProvaDelDNP)
admin.site.register(ProvaDelDP)
admin.site.register(TrendLiquidazione)
admin.site.register(ProfiloRilevante)
admin.site.register(TrendProfiloRilevante)
admin.site.register(TrendProfiloRilevanteContainer)
admin.site.register(User)
