# Generated by Django 2.2.10 on 2020-05-17 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoemails', '0009_auto_20200223_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trigger',
            name='action',
            field=models.CharField(choices=[('new-instructor', 'Instructor is added to the workshop'), ('week-after-workshop-completion', '7 days past the end date of an active workshop'), ('self-organised-request-form', 'A new event is created from Self-Organised Request Form'), ('instructors-host-introduction', 'Introduction of instrutors and host (centr. org. workshop)')], max_length=50, verbose_name='Action'),
        ),
    ]
