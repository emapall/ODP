# Generated by Django 3.0.6 on 2021-02-11 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odp_app', '0012_auto_20210211_1629'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ctu',
            old_name='citazioni_bibliografice',
            new_name='citazioni_bibliografiche',
        ),
        migrations.AlterField(
            model_name='ctu',
            name='danno_differenziale_inail',
            field=models.TextField(blank=True, default='', verbose_name='Danno differenziale inail'),
        ),
        migrations.AlterField(
            model_name='ctu',
            name='riferimento_valutativo_arg',
            field=models.TextField(blank=True, default='', help_text='Specificare se necessario, altrimenti si può lasciare in bianco.', verbose_name='Riferimento valutativo - specificare'),
        ),
    ]