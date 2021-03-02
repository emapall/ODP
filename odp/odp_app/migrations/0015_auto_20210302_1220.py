# Generated by Django 3.0.6 on 2021-03-02 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('odp_app', '0014_auto_20210302_1212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ctu',
            name='infortunato',
        ),
        migrations.AddField(
            model_name='ctu',
            name='sentenza',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='odp_app.Sentenza', verbose_name='Sentenza'),
        ),
    ]
