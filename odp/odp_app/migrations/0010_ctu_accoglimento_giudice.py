# Generated by Django 3.0.6 on 2021-02-11 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odp_app', '0009_auto_20210211_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='ctu',
            name='accoglimento_giudice',
            field=models.SmallIntegerField(choices=[(0, 'Altro (specificare)'), (1, 'Tabella Comm. Min. ex DM 26/5/2004'), (2, 'Linee guida SIMLA 2016'), (3, 'Ronchi et al, 2015'), (4, 'Tabelle DM 3/7/03')], default=0, verbose_name='Accoglimento giudice'),
            preserve_default=False,
        ),
    ]