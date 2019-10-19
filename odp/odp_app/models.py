# -*- coding: utf-8 -*-

############################################################
#
#  Aggiunto campo pre2001 a Infortunato      [JC 17/03/2007]
#  Modificati campi calcolati in Infortunato [JC 28/03/2007]
#  Tolto campo accoglimento, rivisti campi ctu [AA 18/05/2007]
#  Aggiunto campo pubblicabile               [JC 18/05/2007]
#  Richiesta parte attrice -> ManyToMany     [JC 22/05/2007]
#  Postumo_tabulato                          [JC 13/06/2007]
#  colpa convenuto -> attore                 [JC 14/06/2007]
#  via infodesc                              [AA 15/06/2007]
#  forza_esclusione per sentenze
#  (anche escluse dalla ricerca)             [JC 22/04/2008]
#  DirittoInviolabile e DannoPatrimonaile    [JC 01/03/2009]
#
############################################################

from django.db import models
from django.template.defaultfilters import date
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# User registration with confirmation email
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    # TODO vedere di sistemare Nome e Cognome
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()


# DipendeDa_est_it = validators.AnyValidator([validators.isNotEmpty, validators.ValidateIfOtherFieldEquals('est_it', 'False', [])])
# DipendeDa_est_ip = validators.AnyValidator([validators.isNotEmpty, validators.ValidateIfOtherFieldEquals('est_ip', 'False', [])])
# DipendeDa_est_lcit = validators.AnyValidator([validators.isNotEmpty, validators.ValidateIfOtherFieldEquals('est_lcit', 'False', [])])
# DipendeDa_est_lcip = validators.AnyValidator([validators.isNotEmpty, validators.ValidateIfOtherFieldEquals('est_lcip', 'False', [])])
# DipendeDa_est_dm = validators.AnyValidator([validators.isNotEmpty, validators.ValidateIfOtherFieldEquals('est_dm', 'False', [])])
# DipendeDa_est_dmip = validators.AnyValidator([validators.isNotEmpty, validators.ValidateIfOtherFieldEquals('est_dmip', 'False', [])])
# DipendeDa_est_dmit = validators.AnyValidator([validators.isNotEmpty, validators.ValidateIfOtherFieldEquals('est_dmit', 'False', [])])
# DipendeDa_est_ss = validators.AnyValidator([validators.isNotEmpty, validators.ValidateIfOtherFieldEquals('est_ss', 'False', [])])

# tabelle legate a Sentenza

# tabelle ManyToMany


class Esaminatore(models.Model):
    esaminatore = models.CharField(max_length=50)

    def __str__(self):
        return self.esaminatore

    class Meta:
        verbose_name = u"esaminatore"
        verbose_name_plural = u"esaminatori"
        ordering = ("esaminatore",)


class Osservatorio(models.Model):
    osservatorio = models.CharField(max_length=50)

    def __str__(self):
        return self.osservatorio

    class Meta:
        verbose_name = u"osservatorio"
        verbose_name_plural = u"osservatori"
        ordering = ("osservatorio",)


class Assicurazione(models.Model):
    assicurazione = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.assicurazione

    class Meta:
        verbose_name = u"assicurazione"
        verbose_name_plural = u"assicurazioni"
        ordering = ("assicurazione",)


# tabelle in ForeignKey


class Regione(models.Model):
    regione = models.CharField(max_length=50)

    def __str__(self):
        return self.regione

    class Meta:
        verbose_name = u"regione"
        verbose_name_plural = u"regioni"
        ordering = ("regione",)


class Provincia(models.Model):
    targa = models.CharField(max_length=2, null=True, blank=False)
    provincia = models.CharField(max_length=50, null=True, blank=False, db_index=True)
    regione = models.ForeignKey(
        Regione, verbose_name="regione", on_delete=models.PROTECT
    )

    def __str__(self):
        return self.provincia + u" - " + self.regione.regione

    class Meta:
        verbose_name = u"provincia"
        verbose_name_plural = u"province"
        ordering = ("provincia",)


class Comune(models.Model):
    codice = models.CharField(max_length=4)
    comune = models.CharField(max_length=50, db_index=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT)

    def __str__(self):
        return self.comune + u" - " + self.provincia.targa

    class Meta:
        verbose_name = u"comune"
        verbose_name_plural = u"comuni"
        ordering = ("comune", "provincia")


class Provenienza(models.Model):
    provenienza = models.CharField(max_length=50)

    def __str__(self):
        return self.provenienza

    class Meta:
        verbose_name = u"provenienza"
        verbose_name_plural = u"provenienze"
        ordering = ("provenienza",)


# tabelle legate a Infortunato

### tabelle ManyToMany


class Lesione(models.Model):
    lesione = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.lesione

    class Meta:
        verbose_name = u"lesione"
        verbose_name_plural = u"lesioni"
        ordering = ("lesione",)


class Postumo(models.Model):
    postumo = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.postumo

    class Meta:
        verbose_name = u"postumo"
        verbose_name_plural = u"postumi"
        ordering = ("postumo",)


class Postumo_tabulato(models.Model):
    postumo_tabulato = models.CharField(max_length=150, db_index=True)

    def __str__(self):
        return self.postumo_tabulato

    class Meta:
        verbose_name = u"postumo da tabella standard"
        verbose_name_plural = u"postumi da tabella standard"
        ordering = ("id",)


class RichiestaParteAttrice(models.Model):
    richiesta = models.CharField(max_length=100)

    def __str__(self):
        return self.richiesta

    class Meta:
        verbose_name = u"richiesta parte attrice"
        verbose_name_plural = u"richieste parte attrice"
        ordering = ("richiesta",)


class DannoPatrimoniale(models.Model):
    tipo = models.CharField(max_length=100)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = u"danno patrimoniale"
        verbose_name_plural = u"danni patrimoniali"
        ordering = ("tipo",)


# il nome della classe resta quello vecchio, ma questi diritti non sono inviolabili 09-04-14
class DirittoInviolabile(models.Model):
    diritto = models.CharField(max_length=100)

    def __str__(self):
        return self.diritto

    class Meta:
        verbose_name = u"diritto"
        verbose_name_plural = u"diritti"
        ordering = ("diritto",)


### tabelle in ForeignKey


class Professione(models.Model):
    professione = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.professione

    class Admin:
        search_fields = ["professione"]

    class Meta:
        verbose_name = u"professione"
        verbose_name_plural = u"professioni"
        ordering = ("professione",)


class Responsabilita(models.Model):
    responsabilita = models.CharField(max_length=80)

    def __str__(self):
        return self.responsabilita

    class Admin:
        search_fields = ["responsabilita"]

    class Meta:
        verbose_name = u"responsabilità"
        verbose_name_plural = u"responsabilità"
        ordering = ("responsabilita",)


class FattoreLiquidazione(models.Model):
    fattore = models.CharField(max_length=100)

    def __str__(self):
        return self.fattore

    class Admin:
        search_fields = ["fattore"]

    class Meta:
        verbose_name = u"fattore rilevante di liquidazione del danno non patrimoniale"
        verbose_name_plural = (
            u"fattori rilevanti di liquidazione del danno non patrimoniale"
        )
        ordering = ("fattore",)


class FattoreLiquidazioneDP(models.Model):
    fattore = models.CharField(max_length=100)

    def __str__(self):
        return self.fattore

    class Admin:
        search_fields = ["fattore"]

    class Meta:
        verbose_name = u"fattore rilevante di liq. del dp"
        verbose_name_plural = u"fattori rilevanti di liq. del dp"
        ordering = ("fattore",)


class ProvaDelDNP(models.Model):
    prova = models.CharField(max_length=100)

    def __str__(self):
        return self.prova

    class Admin:
        search_fields = ["prova"]

    class Meta:
        verbose_name = u"prova del danno non patrimoniale"
        verbose_name_plural = u"prove del danno non patrimoniale"
        ordering = ("prova",)


class ProvaDelDP(models.Model):
    prova = models.CharField(max_length=100)

    def __str__(self):
        return self.prova

    class Admin:
        search_fields = ["prova"]

    class Meta:
        verbose_name = u"prova del danno patrimoniale"
        verbose_name_plural = u"prove del danno patrimoniale"
        ordering = ("prova",)


class TrendLiquidazione(models.Model):
    trend = models.CharField(max_length=100)

    def __str__(self):
        return self.trend

    class Admin:
        search_fields = ["trend"]

    class Meta:
        verbose_name = u"trend di liquidazione"
        verbose_name_plural = u"trend di liquidazione"
        ordering = ("trend",)


class TrendProfiloRilevante(models.Model):
    trend = models.CharField(max_length=80)

    def __str__(self):
        return self.trend

    class Meta:
        verbose_name = u"trend profilo rilevante"
        verbose_name_plural = u"trend profili rilevanti"
        ordering = ("trend",)


class ProfiloRilevante(models.Model):
    profilo = models.CharField(max_length=80)
    trend = models.ForeignKey(
        TrendProfiloRilevante, null=True, blank=True, on_delete=models.PROTECT
    )

    def __str__(self):
        return self.profilo

    class Admin:
        search_fields = ["profilo"]

    class Meta:
        verbose_name = u"profilo rilevante"
        verbose_name_plural = u"profili rilevanti"
        ordering = ("trend", "profilo")


## Tabella Sentenza ##


class Sentenza(models.Model):

    # Elementi delle caselle di scelta:
    # TODO: Eliminare "--nessuno--"?
    GRADO_DI_GIUDIZIO = (
        ("", "--nessuno--"),
        ("C", "Corte d'Appello"),
        ("P", "Giudice di Pace"),
        ("T", "Tribunale"),
        ("R", "T.A.R."),
        ("S", "Consiglio di Stato"),
    )
    RICONVENZIONALE = (
        ("A", "Accolta"),
        ("P", "Parz. accolta"),
        ("R", "Rigettata"),
        ("S", "Assente"),
    )
    # RESPONSABILITA = (
    #    ('D', 'Dolo'),
    #    ('A', 'Colpa esclusiva dell\'attore'),
    #    ('E', 'Colpa esclusiva del convenuto'),
    #    ('C', 'Colpa concorrente del convenuto'),
    #    ('O', 'Colpa concorrente dell\'attore'),
    #    ('1', 'Presunzione di responsabilità ex 2054 cc I comma'),
    #    ('2', 'Presunzione di responsabilità ex 2054 cc II comma'),
    # )

    # Campi della tabella
    # TODO: IntegerField -> Positive[Small]IntegerField ?
    #       Togliere NULL ovunque possibile?
    grado_di_giudizio = models.CharField(
        "grado di giudizio",
        max_length=1,
        default="",
        choices=GRADO_DI_GIUDIZIO,
        null=False,
        blank=False,
    )
    numero_della_sezione = models.IntegerField(
        "numero della sezione", null=False, blank=False, default=0
    )
    data_del_fatto = models.DateField("data fatto", null=True, blank=True)
    data_della_citazione = models.DateField("data citazione", null=True, blank=True)
    data_della_sentenza = models.DateField("data sentenza", null=True, blank=True)
    data_del_deposito = models.DateField("data deposito", null=True, blank=True)
    numero_della_sentenza = models.IntegerField(
        "numero della sentenza", null=False, blank=False
    )
    esaminatore = models.ManyToManyField(
        Esaminatore, verbose_name="esaminatore", null=True, blank=False
    )
    osservatorio = models.ManyToManyField(
        Osservatorio, verbose_name="osservatorio", null=True, blank=False
    )
    estensore = models.CharField("estensore", max_length=50, null=False, blank=False)
    riconvenzionale = models.CharField(
        "riconvenzionale",
        max_length=1,
        choices=RICONVENZIONALE,
        null=False,
        blank=False,
    )

    # Ridondante ma necessario -> JavaScript?
    anno_del_deposito = models.IntegerField("anno deposito", null=True, blank=True)

    # IL GRUPPO CHE SEGUE DOVRA' ESSERE ELIMINATO (sostituiti dal campo "profili_rilevanti")
    #    so = models.BooleanField('ordinaria')
    #    si_it = models.BooleanField('invalidità temporanea')
    #    si_ip = models.BooleanField('invalidità permanente')
    #    si_dm = models.BooleanField('danno morale')
    #    si_mo = models.BooleanField('danno da morte')
    #    si_rp = models.BooleanField('responsabilità professionale')
    #    si_de = models.BooleanField('danno non patrimoniale')
    #    si_codice_assicurazioni = models.BooleanField('codice assicurazioni')
    #    si_altro = models.BooleanField('altro')

    estctu = models.BooleanField("ctu allegata")
    #    profili_rilevanti = models.ManyToManyField(ProfiloRilevante, verbose_name='profili rilevanti', null=True, blank=True)
    note_profili_rilevanti = models.TextField(
        "note ai profili rilevanti", null=True, blank=True
    )

    anno_di_arrivo = models.PositiveIntegerField("anno arrivo", null=True, blank=False)

    codice = models.CharField("Codice archivio", max_length=50, null=True, blank=True)
    sede_tribunale = models.ForeignKey(
        Comune,
        verbose_name="sede tribunale",
        null=True,
        blank=False,
        on_delete=models.PROTECT,
    )
    assicurazione = models.ManyToManyField(
        Assicurazione, verbose_name="assicurazione", null=True, blank=False
    )  # filter_interface=models.HORIZONTAL,
    provenienza = models.ForeignKey(
        Provenienza,
        verbose_name="provenienza",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    numero_attori = models.IntegerField(
        "numero attori", default=0, null=True, blank=False
    )
    numero_convenuti = models.IntegerField(
        "numero convenuti", default=0, null=True, blank=False
    )
    numero_terzi = models.IntegerField(
        "numero terzi", default=0, null=True, blank=False
    )
    fatto = models.TextField("fatto", null=False, blank=False)
    responsabilita = models.ForeignKey(
        Responsabilita,
        verbose_name="responsabilità",
        null=True,
        blank=False,
        on_delete=models.PROTECT,
    )
    note_sentenza = models.TextField("note", null=False, blank=True)
    ocr = models.TextField("ocr", null=False, blank=True)
    file_img = models.FileField(
        "immagine", upload_to="immagine/", null=True, blank=True
    )
    file_sch = models.FileField(
        "scheda riassuntiva", upload_to="scheda/", null=True, blank=True
    )
    file_cmn = models.FileField(
        "scheda di commento", upload_to="commento/", null=True, blank=True
    )

    # Flag se escludere la sentenza dalla vista del mondo
    forza_esclusione = models.BooleanField(
        "Rendi la sentenza non pubblicabile, indipendentemente dalle schede infortunato",
        default=False,
    )

    def __str__(self):
        #        if (self.file_img == '') and (self.file_sch == '') and (self.file_cmn == ''):
        #            linestr = '(no file) '
        #        else:
        #            if self.file_img <> '':
        #                link = self.file_img
        #                linestr = '(' + link[1+link.rfind('/'):link.rfind('.')] + ') '
        #            elif self.file_sch <> '':
        #                link = self.file_sch
        #                linestr = '(' + link[1+link.rfind('/'):link.rfind('.')] + ') '
        #            else:
        #                link = self.file_cmn
        #                linestr = '(' + link[1+link.rfind('/'):link.rfind('.')] + ') '

        if self.grado_di_giudizio == u"":
            linestr = self.sede_tribunale.comune
        else:
            linestr = (
                self.get_grado_di_giudizio_display()
                + u" di "
                + self.sede_tribunale.comune
            )

        if self.data_della_sentenza:
            linestr += u" (" + date(self.data_della_sentenza, "j/m/Y") + u")"
        elif self.data_del_deposito:
            linestr += u" (" + date(self.data_del_deposito, "j/m/Y") + u")"
        elif self.data_della_citazione:
            linestr += u" (" + date(self.data_della_citazione, "j/m/Y") + u")"
        return linestr

    def files_allegati(self):
        return (self.file_img != "") or (self.file_sch != "") or (self.file_cmn != "")
        files_allegati.short_description = "PDF"

    def save(self):
        if self.data_del_deposito:
            self.anno_del_deposito = self.data_del_deposito.year
        super(Sentenza, self).save()

    class Meta:
        #        permissions = (
        #            ("can_upload", "Can upload files"),
        #        )
        verbose_name = u"sentenza"
        verbose_name_plural = u"sentenze"
        ordering = ("-anno_di_arrivo", "-data_della_sentenza")


class Infortunato(models.Model):

    ENTE_SOCIALE = (
        ("", "(non specificato)"),
        ("INAIL", "INAIL"),
        ("INAIL- RESPINTA", "INAIL- RESPINTA"),
        ("INAL", "INAL"),
        ("INAM", "INAM"),
        ("INPS", "INPS"),
        ("INPS - INAIL", "INPS - INAIL"),
        ("INPS-INAM", "INPS-INAM"),
        ("MINISTERO PP. TT.", "MINISTERO PP. TT."),
    )
    TIPO_RIVALUTAZIONE = (
        ("0", "Nessuna"),
        ("1", "Data del fatto"),
        ("2", "Data della citazione"),
        ("3", "Data della pubblicazione"),
        ("4", "Altro"),
    )
    DASIT = (
        ("0", "Non ricavabile"),
        ("1", "Triplo Pensione Sociale"),
        ("3", "Via Equitativa Pura"),
        ("4", "IN IP"),
        ("5", "ALTRO"),
        ("6", "Euro al dì"),
        ("7", "TAB"),
        ("8", "Legge 57/2001"),
        ("9", "Codice Assicurazioni"),
    )
    LCIT = (
        ("0", "Non ricavabile"),
        ("1", "Reddito dimostrato"),
        ("2", "Reddito presunto triplo pensione sociale"),
        ("3", "Reddito medio nazionale"),
        ("4", "Via equitativa pura"),
        ("5", "ALTRO"),
    )
    DASIP = (
        ("0", "Non ricavabile"),
        ("1", "Calcolo a Punto"),
        ("2", "Triplo Pensione Sociale"),
        ("4", "Via equitativa Pura"),
        ("5", "ALTRO"),
        ("3", "Reddito medio nazionale"),
        ("7", "Legge 57 / 2001"),
        ("8", "Codice Assicurazioni"),
    )
    LCIP = (
        ("0", "Non ricavabile"),
        ("1", "Reddito dimostrato"),
        ("2", "Reddito dimostrato capitalizzato"),
        ("3", "RDD.FND PRS"),
        ("4", "Reddito presunto triplo pensione sociale"),
        ("5", "Reddito presunto Reddito medio nazionale"),
        ("6", "Reddito presunto figurato"),
        ("7", "via equitativa pura"),
        ("8", "ALTRO"),
        ("9", "Calcolo a punto"),
    )
    TIPO_LESIONE = (("S", "Singola"), ("C", "Complessa"), ("N", "Non pervenuto"))
    ACCOGLIMENTO = (("S", "Sì"), ("N", "No"), ("P", "Parzialmente"))
    TIPO_CTU = (
        ("00", ""),
        ("01", "Medico Legale"),
        ("02", "Medico Legale Plurispecialista"),
        ("03", "Altre Spec. Omogenea"),
        ("04", "Altre Spec. Non Omogenea"),
        ("05", "Medico Generico"),
        ("06", "Non ricavabile"),
    )
    TIPO_QUESITO = (
        ("00", ""),
        ("01", "Riportato"),
        ("02", "Deducibile"),
        ("03", "Non Deducibile"),
    )
    RESOCONTO_OP_PERITALI = (
        ("00", ""),
        ("01", "No"),
        ("02", "Sintetico"),
        ("03", "Dettagliato"),
    )
    TIPO_CTP = (
        ("00", ""),
        ("01", "Nominati"),
        ("02", "Non Nominati"),
        ("03", "Non Ricavabile"),
    )
    MAGGIORENNE = (("0", "Minorenne"), ("1", "Maggiorenne"), ("2", "(non ricavabile)"))
    SESSO = (("M", "Maschio"), ("F", "Femmina"), ("N", "(non ricavabile)"))
    TIPO_SR = (("S", "Surroga"), ("R", "Regresso"))
    CTP_NOMINATI = (
        ("00", ""),
        ("01", "Richieste CTP riportate in CTU"),
        ("02", "Richieste CTP non riportate"),
        ("03", "CTP in accordo con CTU"),
    )
    TIPO_DOC_MEDICA = (
        ("00", ""),
        ("01", "Assente"),
        ("02", "Insufficiente"),
        ("03", "Sintetica"),
        ("04", "Dettagliata"),
    )
    TIPO_ANA_GENERALE = (
        ("00", ""),
        ("01", "Sintetica"),
        ("02", "Dettagliata"),
        ("03", "Indifferente"),
        ("04", "Assente"),
    )
    TIPO_ANA_LAVORATIVA = (
        ("00", ""),
        ("01", "Sintetica"),
        ("02", "Dettagliata"),
        ("03", "Solo lavoro attuale"),
        ("04", "Assente"),
    )
    TIPO_STATO_ATTUALE = (
        ("00", ""),
        ("01", "Sintetico"),
        ("02", "Dettagliato"),
        ("03", "Insufficiente"),
        ("04", "Periziando deceduto"),
    )
    TIPO_EO_GENERALE = (
        ("00", ""),
        ("01", "Assente"),
        ("02", "Indifferente"),
        ("03", "Sintetico"),
        ("04", "Dettagliato"),
        ("05", "P. deceduto"),
    )
    TIPO_EO_SPECIFICO = (
        ("00", ""),
        ("01", "Assente"),
        ("02", "Sintetico"),
        ("03", "Dettagliato"),
        ("04", "P. deceduto"),
    )
    FLAG_VIS_SPEC = (("00", ""), ("Si", "Sì"), ("No", "No"))
    TIPO_ESAMI_STRUMENTALI = (
        ("00", ""),
        ("01", "Assenti"),
        ("02", "In atti"),
        ("03", "Portati dal periziando"),
        ("04", "Richiesti dal CTU"),
        ("05", "In atti - portati dal periz."),
        ("06", "In atti - richiesti dal CTU"),
        ("07", "Portati dal per. - Rich. CTU"),
    )
    TIPO_TRAT_ML = (
        ("00", ""),
        ("01", "Assente"),
        ("02", "Insufficiente breve"),
        ("03", "Insufficiente lunga"),
        ("04", "Esaustiva sintetica"),
        ("05", "Esaustiva dettagliata"),
    )
    TIPO_RISPOSTA_QUESITI = (("00", ""), ("01", "Completa"), ("02", "Incompleta"))

    # campi della tabella

    sentenza = models.ForeignKey(
        Sentenza,
        verbose_name="sentenza",
        related_name="infortunati",
        on_delete=models.PROTECT,
    )
    eta = models.IntegerField("età", null=True, blank=True)
    est_maggiorenne = models.CharField(
        "est maggiorenne", max_length=1, choices=MAGGIORENNE, null=True, blank=False
    )
    sesso = models.CharField(
        "sesso", max_length=1, choices=SESSO, null=True, blank=False
    )
    professione = models.ForeignKey(
        Professione, verbose_name="professione", on_delete=models.PROTECT
    )
    percentuale_colpa_attore = models.DecimalField(
        "percentuale colpa attore",
        decimal_places=2,
        max_digits=5,
        null=True,
        blank=False,
    )
    ente_sociale = models.CharField(
        "ente sociale", max_length=25, choices=ENTE_SOCIALE, null=True, blank=True
    )
    tipo_sr = models.CharField(
        "tipo surroga", max_length=1, choices=TIPO_SR, null=True, blank=True
    )
    importo_sr = models.DecimalField(
        "importo surroga", decimal_places=2, max_digits=20, null=True, blank=True
    )

    ##### campi tra tonde da inserire qua #????

    importo_provvisionale = models.DecimalField(
        "importo acconto", decimal_places=2, max_digits=20, null=True, blank=False
    )
    tipo_rivalutazione = models.CharField(
        "tipo rivalutazione",
        max_length=1,
        choices=TIPO_RIVALUTAZIONE,
        null=True,
        blank=False,
    )

    interessi_legali_it = models.DateField(
        "interessi legali invalidità temporanea", null=True, blank=True
    )
    interessi_legali_ip = models.DateField(
        "interessi legali invalidità permanente", null=True, blank=True
    )
    interessi_legali_dm = models.DateField(
        "interessi legali danni morali", null=True, blank=True
    )
    interessi_legali_ss = models.DateField(
        "interessi legali spese sostenute", null=True, blank=True
    )
    interessi_legali_dc = models.DateField(
        "interessi legali danni alle cose", null=True, blank=True
    )
    interessi_legali_lcit = models.DateField(
        "interessi legali lucro cessante invalidità temporanea", null=True, blank=True
    )
    interessi_legali_lcip = models.DateField(
        "interessi legali lucro cessante invalidità permanente", null=True, blank=True
    )
    # importo_danni_cose=models.DecimalField('importo danni alle cose', decimal_places=2, max_digits=20, null=True, blank=True)
    # importo_altri_danni=models.DecimalField('importo altri danni', decimal_places=2, max_digits=20, null=True, blank=True)

    est_it = models.BooleanField("c'è invalidità temporanea")
    est_das_it = models.CharField(
        "danno biologico da invalidità temporanea",
        max_length=1,
        null=True,
        blank=True,
        editable=False,
    )
    metodo_das_it = models.CharField(
        "metodo das it", max_length=1, choices=DASIT, null=True, blank=True
    )
    importo_liquidazione_das_it = models.DecimalField(
        "importo liquidazione das it",
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
    )
    euro_al_di = models.DecimalField(
        "euro al dì", decimal_places=2, max_digits=20, null=True, blank=True
    )
    est_lcit = models.BooleanField(
        "c'è lucro cessante da invalidità temporanea", null=False, blank=True
    )
    metodo_lcit = models.CharField(
        "metodo lucro cessante da invalidità temporanea",
        max_length=1,
        choices=LCIT,
        null=True,
        blank=True,
    )
    importo_liquidazione_lcit = models.DecimalField(
        "importo lucro cessante da invalidità temporanea",
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
    )
    giorni_lcit = models.IntegerField(
        "giorni lucro cessante da invalidità temporanea", null=True, blank=True
    )

    est_ip = models.BooleanField("c'è invalidità permanente")
    est_das_ip = models.CharField(
        "danno biologico da invalidità permanente", max_length=1, null=True, blank=True
    )
    metodo_das_ip = models.CharField(
        "metodo das ip", max_length=1, choices=DASIP, null=True, blank=True
    )
    percentuale_das_ip = models.DecimalField(
        "percentuale das ip", decimal_places=2, max_digits=5, null=True, blank=True
    )
    importo_liquidazione_das_ip = models.DecimalField(
        "importo liquidazione das ip",
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
    )
    est_lcip = models.BooleanField(
        "c'è lucro cessante da invalidità permanente", null=False, blank=True
    )
    metodo_lcip = models.CharField(
        "metodo lucro cessante da invalidità permanente",
        max_length=1,
        choices=LCIT,
        null=True,
        blank=True,
    )
    percentuale_lcip = models.DecimalField(
        "percentuale", decimal_places=2, max_digits=5, null=True, blank=True
    )
    importo_liquidazione_lcip = models.DecimalField(
        "importo lucro cessante da invalidità permanente",
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
    )

    est_clg = models.BooleanField("est capacità lavorativa generica")
    est_cls = models.BooleanField("est capacità lavorativa specifica")
    est_dm = models.BooleanField("c'è danno morale")
    motivazione = models.CharField("motivazione", max_length=255, null=True, blank=True)

    # campi liberi aggiunti il 5/5/14 YV
    metodo_di_quantificazione = models.CharField(
        "metodo di quantificazione", max_length=255, null=True, blank=True
    )
    periodo_di_sopravvivenza = models.CharField(
        "periodo di sopravvivenza", max_length=255, null=True, blank=True
    )
    criterio_liquidazione = models.CharField(
        "criterio di liquidazione", max_length=255, null=True, blank=True
    )
    est_rdjh = models.BooleanField("est riconoscimento danno jure haereditario")
    est_pddb = models.BooleanField("est personalizzazione del danno biologico")
    est_interazione = models.BooleanField(
        "est interazione tra risarcimento danno patrimoniale e risarcimento danno non patrimoniale"
    )
    sunt_diritti_lesi = models.BooleanField("ci sono diritti lesi")

    percentuale_pddb = models.DecimalField(
        "% danno", decimal_places=2, max_digits=5, null=True, blank=True
    )

    # NOTA: E' solo uno dei componenti... totaleDanniMorali = importo_liquidazione_dm + importo_liquidazione_dmit + importo_liquidazione_dmip
    importo_liquidazione_dm = models.DecimalField(
        "importo liquidazione danni morali",
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
    )

    est_dm_vp = models.BooleanField("via equitativa pura")
    est_dm_it = models.BooleanField("da invalidità temporanea")
    est_dm_ip = models.BooleanField("da invalidità permanente")
    importo_liquidazione_dmit = models.DecimalField(
        "Importo danni morali da I.T.",
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
    )
    durata_dmit = models.IntegerField(
        "Durata danni morali da I.T.", null=True, blank=True
    )
    importo_liquidazione_dmip = models.DecimalField(
        "importo danni morali da I.P.",
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
    )
    percentuale_dmip = models.DecimalField(
        "% danni morali da I.P.", decimal_places=2, max_digits=5, null=True, blank=True
    )
    est_ss = models.BooleanField("risarcite spese sostenute")
    est_ss_sostenute = models.BooleanField("risarcite spese già sostenute")
    importo_sostenute = models.DecimalField(
        "importo spese già sostenute",
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
    )
    est_ss_future = models.BooleanField("risarcite spese future")
    importo_future = models.DecimalField(
        "importo spese future", decimal_places=2, max_digits=20, null=True, blank=True
    )
    importo_danni_cose = models.DecimalField(
        "importo danni alle cose",
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
    )
    importo_altri_danni = models.DecimalField(
        "importo altri danni", decimal_places=2, max_digits=20, null=True, blank=True
    )
    altri_danni = models.TextField("altri danni", null=True, blank=True)
    tipo_lesione = models.CharField(
        "tipo lesione", max_length=1, choices=TIPO_LESIONE, null=True, blank=False
    )
    accoglimento_giudice = models.CharField(
        "accoglimento giudice",
        max_length=1,
        choices=ACCOGLIMENTO,
        null=True,
        blank=True,
    )
    # mettere una lista?
    qualifica_ctu = models.CharField(
        "qualifica ctu", max_length=25, null=True, blank=True
    )
    tabella = models.BooleanField("tabella")
    sede_tabella = models.CharField(
        "sede tabella", max_length=25, null=True, blank=True
    )
    note_fattori_rilevanti_liquidazione = models.TextField(
        "note ai fattori rilevanti di liquidazione del danno non patrimoniale",
        null=True,
        blank=True,
    )
    note_fattori_rilevanti_liquidazione_dp = models.TextField(
        "note ai fattori rilevanti di liquidazione del danno patrimoniale",
        null=True,
        blank=True,
    )

    richiestaparteattrice = models.ManyToManyField(
        RichiestaParteAttrice,
        null=False,
        blank=False,
        verbose_name="Richiesta parte attrice",
    )

    dm_est = models.BooleanField("est danno da morte")
    dm_dbjh_est = models.BooleanField("est danno biologico jure hereditario")
    dm_dbjh_importo_liquidazione = models.DecimalField(
        "importo liquidazione danno biologico jure hereditario",
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
    )
    # est_de =                       models.BooleanField('est danno non patrimoniale da perdita del congiunto')
    # importo_liquidazione_de =      models.DecimalField('importo liquidazione danno non patrimoniale', decimal_places=2, max_digits=20, null=True, blank=True)
    # interessi_legali_de =          models.DateField('interessi legali danno non patrimoniale', null=True, blank=True)

    # TODO: Elimina?
    # eliminata dal db 9mag2014
    # voci_biblio = models.BooleanField('voci biblio')

    # controllare acc giudice
    # accoglimento=models.CharField('accoglimento giudice', max_length=2, null=True, blank=True)
    tipo_ctu = models.CharField(
        "tipo ctu", max_length=2, choices=TIPO_CTU, null=True, blank=True
    )
    tipo_quesito = models.CharField(
        "tipo quesito", max_length=2, choices=TIPO_QUESITO, null=True, blank=True
    )
    resoconto_op_per = models.CharField(
        "resoconto op peritali",
        max_length=2,
        choices=RESOCONTO_OP_PERITALI,
        null=True,
        blank=True,
    )
    tipo_ctp = models.CharField(
        "tipo ctp", max_length=2, choices=TIPO_CTP, null=True, blank=True
    )

    ctp_nominati = models.CharField(
        "ctp nominati", max_length=2, choices=CTP_NOMINATI, null=True, blank=True
    )
    tipo_doc_medica = models.CharField(
        "tipo documentazione medica",
        max_length=2,
        choices=TIPO_DOC_MEDICA,
        null=True,
        blank=True,
    )
    tipo_ana_generale = models.CharField(
        "tipo anamnesi generale",
        max_length=2,
        choices=TIPO_ANA_GENERALE,
        null=True,
        blank=True,
    )
    tipo_ana_lavorativa = models.CharField(
        "tipo anamnesi lavorativa",
        max_length=2,
        choices=TIPO_ANA_LAVORATIVA,
        null=True,
        blank=True,
    )
    tipo_stato_attuale = models.CharField(
        "tipo stato attuale",
        max_length=2,
        choices=TIPO_STATO_ATTUALE,
        null=True,
        blank=True,
    )
    tipo_eo_generale = models.CharField(
        "tipo esame obiettivo generale",
        max_length=2,
        choices=TIPO_EO_GENERALE,
        null=True,
        blank=True,
    )
    tipo_eo_specifico = models.CharField(
        "tipo esame obiettivo specifico",
        max_length=2,
        choices=TIPO_EO_SPECIFICO,
        null=True,
        blank=True,
    )
    # TODO:checkbox (sì/ no)
    flag_vis_spec = models.CharField(
        "richiesta visita specialistica",
        max_length=2,
        choices=FLAG_VIS_SPEC,
        null=True,
        blank=True,
    )
    tipo_esami_strumentali = models.CharField(
        "tipo esami strumentali",
        max_length=2,
        choices=TIPO_ESAMI_STRUMENTALI,
        null=True,
        blank=True,
    )
    tipo_trat_ml = models.CharField(
        "tipo trattazione medico legale",
        max_length=2,
        choices=TIPO_TRAT_ML,
        null=True,
        blank=True,
    )
    tipo_risposta_quesiti = models.CharField(
        "tipo risposta quesiti",
        max_length=2,
        choices=TIPO_RISPOSTA_QUESITI,
        null=True,
        blank=True,
    )
    # TODO: lista a scelta multipla?
    tipo_quesito_ndc = models.BooleanField("CTU - Nesso di causa")
    tipo_quesito_sa = models.BooleanField("CTU - stato anteriore")
    tipo_quesito_t = models.BooleanField("CTU - invalidità temporanea")
    tipo_quesito_db = models.BooleanField("CTU - danno biologico")
    tipo_quesito_clg = models.BooleanField("CTU - capacità lavorativa generica")
    tipo_quesito_cls = models.BooleanField("CTU - capacità lavorativa specifica")
    tipo_quesito_de = models.BooleanField("CTU - danno estetico")
    tipo_quesito_ss = models.BooleanField("CTU - spese sostenute")
    tipo_quesito_sf = models.BooleanField("CTU - spese future")

    tipo_fatto_mod = models.BooleanField("tipo fatto mod")
    tipo_fatto_solltra = models.BooleanField("tipo fatto solltra")
    tipo_fatto_primer = models.BooleanField("tipo fatto primer")
    tipo_fatto_ritorno = models.BooleanField("tipo fatto ritorno")

    flag_rif_tabellare = models.BooleanField("c'è riferimento tabellare")
    desc_rif_tabellare = models.TextField(
        "descrizione riferimento tabellare", null=True, blank=True
    )

    note_gen = models.TextField("note al danneggiato", null=True, blank=True)
    note_ctu = models.TextField("note alla CTU", null=True, blank=True)
    note_importi = models.TextField("note importi", null=True, blank=True)
    # note aggiunte
    note_generale = models.TextField("note generale", null=True, blank=True)
    note_it = models.TextField("note invalidità temporanea", null=True, blank=True)
    note_ip = models.TextField("note invalidità permanente", null=True, blank=True)
    # note_morte=models.TextField('note danno da morte', null=True, blank=True)
    note_dm = models.TextField("note danno morale", null=True, blank=True)

    ### campi calcolati ###
    importo_liquidazione_das = models.DecimalField(
        "liquidazione danno alla salute (dasip+dasit)",
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
        editable=False,
    )
    importo_dap = models.DecimalField(
        "totale danni alla persona",
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
        editable=False,
    )
    importo_ad = models.DecimalField(
        "totale altri danni",
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
        editable=False,
    )
    importo_totale = models.DecimalField(
        "totale", decimal_places=2, max_digits=20, null=True, blank=True, editable=False
    )
    importo_liquidato = models.DecimalField(
        "totale liquidato",
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
        editable=False,
    )
    liquidazione_totale = models.DecimalField(
        "liquidazione totale",
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
        editable=False,
    )
    # FIXME: da calcolare?
    importo_rivalutazione = models.DecimalField(
        "importo rivalutazione", decimal_places=2, max_digits=20, null=True, blank=True
    )

    # campi aggiunti per alleggerire le query [JC 17/3/2007]
    pre2001 = models.BooleanField(
        "Risale a prima del 2001", db_index=True, default=False
    )

    # molti a molti
    lesione = models.ManyToManyField(
        Lesione, null=True, blank=True
    )  # filter_interface=models.VERTICAL,
    postumo = models.ManyToManyField(
        Postumo, null=True, blank=True
    )  # filter_interface=models.VERTICAL,
    postumo_tabulato = models.ManyToManyField(Postumo_tabulato, null=True, blank=True)

    # Altri danni patrimoniali
    dannopatrimoniale = models.ManyToManyField(
        DannoPatrimoniale,
        null=True,
        blank=True,
        verbose_name="Altri danni patrimoniali",
    )
    importo_dannopatrimoniale = models.DecimalField(
        "importo liquidato per altri danni patrimoniali",
        decimal_places=2,
        max_digits=20,
        null=True,
        blank=True,
    )
    interessi_dannopatrimoniale = models.DateField(
        "interessi legali per altri danni patrimoniali", null=True, blank=True
    )
    note_dannopatrimoniale = models.TextField(
        "note per altri danni patrimoniali", null=True, blank=True
    )
    note_exaltrespese = models.TextField(
        "note per spese e danni alle cose", null=True, blank=True
    )

    # Lesione diritti inviolabili (vedi email per l'intricaterrima casistica degli 'altri danni')
    # A quanto pare questi diritti non sono così inviolabili - 09-04-14
    dirittoinviolabile = models.ManyToManyField(
        DirittoInviolabile, null=True, blank=True, verbose_name="Diritti lesi"
    )
    importo_dirittoinviolabile = models.DecimalField(
        "importo liquidato", decimal_places=2, max_digits=20, null=True, blank=True
    )
    interessi_dirittoinviolabile = models.DateField(
        "interessi legali", null=True, blank=True
    )
    note_dirittoinviolabile = models.TextField("note", null=True, blank=True)

    # Flag se pubblicabile (se gia' letta dal medico legale)
    pubblicabile = models.BooleanField("Pubblicabile", default=False)

    # Aggiunte di gennaio 2011
    fattori_rilevanti_liquidazione = models.ManyToManyField(
        FattoreLiquidazione,
        null=True,
        blank=True,
        verbose_name="fattori rilevanti di liquidazione del danno non patrimoniale",
    )
    fattori_rilevanti_liquidazione_dp = models.ManyToManyField(
        FattoreLiquidazioneDP,
        null=True,
        blank=True,
        verbose_name="fattori rilevanti di liquidazione del danno patrimoniale",
    )
    prova_del_dnp = models.ManyToManyField(
        ProvaDelDNP,
        null=True,
        blank=True,
        verbose_name="prove del danno non patrimoniale",
    )
    note_prova_del_dnp = models.TextField(
        "note alle prove del danno non patrimoniale", null=True, blank=True
    )
    prova_del_dp = models.ManyToManyField(
        ProvaDelDP, null=True, blank=True, verbose_name="prove del danno patrimoniale"
    )
    note_prova_del_dp = models.TextField(
        "note alle prove del danno patrimoniale", null=True, blank=True
    )
    trend_liquidazione = models.ManyToManyField(
        TrendLiquidazione, null=True, blank=True, verbose_name="trend di liquidazione"
    )
    note_trend_liquidazione = models.TextField(
        "note ai trend di liquidazione", null=True, blank=True
    )

    def __str__(self):
        return str(self.id)
        # if (self.eta != 0) :
        #    return str(self.id) + ' ' + str(self.professione) + '  (et�: ' + str(self.eta) + ')'
        # else :
        #    return str(self.id) + ' ' + str(self.professione)
        # return str(self.eta)+' '+self.sesso+' '+self.nome_infortunato

    def save(self):
        # FIXME: est_das_ip / est_das_it Ridondanti?
        # infatti est_das_* non sono presenti nell'admin
        self.est_das_ip = None
        self.est_das_it = None
        # if (self.est_ip <> None):
        # self.est_das_ip = self.est_ip
        # if (self.est_it <> None):
        # self.est_das_it = self.est_it

        #################################################################################################################
        ### [TODO] Questo NON è un modo sensato di fare validazione... quella è in admin.py. Da controllare con l'ODP.

        # danno morale
        #        if self.est_dm == False or self.est_dm == None:
        #            self.motivazione = None; self.est_dm_vp = False; self.importo_liquidazione_dm = None; self.interessi_legali_dm = None; self.est_dm_it = False; self.est_dm_ip = False; self.note_dm = None
        #        if self.est_dm_it == False or self.est_dm_it == None:
        #            self.durata_dmit = None; self.importo_liquidazione_dmit = None
        #        if self.est_dm_ip == False or self.est_dm_ip == None:
        #            self.percentuale_dmip = None; self.importo_liquidazione_dmip = None
        # inval temporanea
        #        if self.est_it == False or self.est_it == None:
        #            self.metodo_das_it = None; self.euro_al_di = None; self.importo_liquidazione_das_it = None; self.interessi_legali_it = None; self.est_lcit = False; self.note_it = None
        #        if self.est_lcit == False or self.est_lcit == None:
        #            self.giorni_lcit = None; self.metodo_lcit = None; self.importo_liquidazione_lcit = None; self.interessi_legali_lcit = None
        # inval permanente
        #        if self.est_ip == False or self.est_ip == None:
        #            self.percentuale_das_ip = None; self.metodo_das_ip = None; self.importo_liquidazione_das_ip = None; self.interessi_legali_ip = None; self.est_lcip = None; self.est_clg = False; self.est_cls = False; self.note_ip = None
        #        if self.metodo_das_ip <> '9':
        #            self.tabella == False
        #        if self.tabella == False or self.tabella == None:
        #            self.sede_tabella == None
        #        if self.est_lcip == False or self.est_lcip == None:
        #            self.metodo_lcip = None; self.percentuale_lcip = None; self.importo_liquidazione_lcip = None; self.interessi_legali_lcip = None
        # danno da morte
        #        if self.dm_est == False or self.dm_est == None:
        #            self.dm_dbjh_est = False; self.est_de = False; self.note_morte = None
        #        if self.dm_dbjh_est == False or self.dm_dbjh_est == None:
        #            self.dm_dbjh_importo_liquidazione = None
        #        if self.est_de == False or self.est_de == None:
        #            self.importo_liquidazione_de = None; self.interessi_legali_de = None
        # altre spese
        #        if self.est_ss == False or self.est_ss == None:
        #            self.est_ss_sostenute = False; self.est_ss_future = False;
        #        if self.est_ss_sostenute == False or self.est_ss_sostenute == None:
        #            self.importo_sostenute = None; self.interessi_legali_ss = None
        #        if self.est_ss_future == False or self.est_ss_future == None:
        #            self.importo_future = None

        #################################################################################################################

        # tutte ok
        termini = [self.importo_liquidazione_das_it, self.importo_liquidazione_das_ip]
        self.importo_liquidazione_das = sum(termine for termine in termini if termine)

        # in 432, la somma non include dmit e dmip
        termini = [
            self.importo_liquidazione_das,
            self.dm_dbjh_importo_liquidazione,
            self.importo_liquidazione_lcit,
            self.importo_liquidazione_lcip,
            self.importo_liquidazione_dmit,
            self.importo_liquidazione_dmip,
            self.importo_liquidazione_dm,
            self.importo_dirittoinviolabile,
        ]
        self.importo_dap = sum(termine for termine in termini if termine)

        # in 1557, importo_ad è zero e non dovrebbe
        termini = [
            self.importo_danni_cose,
            self.importo_altri_danni,
            self.importo_dannopatrimoniale,
        ]
        self.importo_ad = sum(termine for termine in termini if termine)

        # nei 1557 di sopra, non torna. però torna usando i singoli termini
        termini = [
            self.importo_dap,
            self.importo_sostenute,
            self.importo_future,
            self.importo_ad,
        ]
        self.importo_totale = sum(termine for termine in termini if termine)

        # id=4641 ha la somma proprio sbagliata
        # altre 4028 hanno importo_liquidato=0
        if not self.importo_provvisionale:  # -Null dà errore
            self.importo_provvisionale = 0
        termini = [self.importo_totale, -self.importo_provvisionale]
        self.importo_liquidato = sum(termine for termine in termini if termine)

        # TODO: liquidazione_totale = importo_liquidato - importo_sr?!?
        # Nota: sulla surroga ci sono strane percentuali, rivalutazioni, ...

        # in 4029 non torna,
        # di cui 80 liquidazione_totale=importo_totale - provvisionale,
        # le altre tornano facendo la somma dei sottotermini
        if not self.importo_sr:  # Come sopra
            self.importo_sr = 0
        termini = [self.importo_liquidato, -self.importo_sr]
        self.liquidazione_totale = sum(termine for termine in termini if termine)

        super(Infortunato, self).save()

    class Meta:
        verbose_name = u"danneggiato"
        verbose_name_plural = u"danneggiati"
        # ordering = ["sentenza", "nome_infortunato"]
        # order_with_respect_to = 'sentenza'


class TrendProfiloRilevanteContainer(models.Model):
    trend = models.ForeignKey(
        TrendProfiloRilevante,
        db_index=True,
        verbose_name="parola chiave",
        on_delete=models.PROTECT,
    )
    profili_rilevanti = models.ManyToManyField(
        ProfiloRilevante,
        db_index=True,
        blank=True,
        null=True,
        verbose_name="profili rilevanti",
    )
    sentenza = models.ForeignKey(Sentenza, db_index=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = u"profilo rilevante container"
        verbose_name_plural = u"profili rilevanti containers"


# tabella Invalidita' temporanea


class Invalidita_temporanea(models.Model):
    infortunato = models.ForeignKey(
        Infortunato, verbose_name="danneggiato", on_delete=models.PROTECT
    )
    percentuale = models.DecimalField("%", decimal_places=2, max_digits=5)  # core=True
    giorni = models.IntegerField("giorni")  # core=True

    class Meta:
        verbose_name = u"invalidità temporanea"
        verbose_name_plural = u"invalidità temporanee"
        ordering = ("-percentuale",)
