# Generated by Django 2.0.5 on 2018-07-15 18:29

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0144_person_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileupdaterequest',
            name='country',
            field=django_countries.fields.CountryField(blank=True, default='', max_length=2, verbose_name='Country of residence'),
        ),
    ]