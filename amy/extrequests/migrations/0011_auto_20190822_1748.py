# Generated by Django 2.1.7 on 2019-08-22 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extrequests', '0010_auto_20190818_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopinquiryrequest',
            name='administrative_fee',
            field=models.CharField(blank=True, choices=[('', 'Not sure yet.'), ('nonprofit', 'I am with a government site, university, or other nonprofit. I understand the workshop fee of US$2500, and agree to follow through on The Carpentries invoicing process.'), ('forprofit', 'I am with a corporate or for-profit site. I understand The Carpentries staff will contact me about workshop fees. I will follow through on The Carpentries invoicing process for the agreed upon fee.'), ('member', 'I am with a Member Organisation so the workshop fee does not apply (Instructor travel costs will still apply).'), ('waiver', 'I am requesting a scholarship for the workshop fee (Instructor travel costs will still apply).')], default=None, max_length=20, null=True, verbose_name='Which of the following applies to your payment for the administrative fee?'),
        ),
        migrations.AlterField(
            model_name='workshopinquiryrequest',
            name='institution_restrictions',
            field=models.CharField(blank=True, choices=[('', 'Not sure yet.'), ('no_restrictions', 'No restrictions.'), ('other', 'Other:')], default='', max_length=20, verbose_name='Our instructors live, teach, and travel globally. We understand that institutions may have citizenship or other requirements for employees or volunteers who facilitate workshops. If your institution fits this description, please share your requirements or note that there are no restrictions.'),
        ),
        migrations.AlterField(
            model_name='workshopinquiryrequest',
            name='number_attendees',
            field=models.CharField(blank=True, choices=[('', 'Not sure yet.'), ('10-40', '10-40 (one room, two instructors)'), ('40-80', '40-80 (two rooms, four instructors)'), ('80-120', '80-120 (three rooms, six instructors)')], default=None, help_text="This number doesn't need to be precise, but will help us decide how many instructors your workshop will need. Each workshop must have at least two instructors.", max_length=15, null=True, verbose_name='Anticipated number of attendees'),
        ),
        migrations.AlterField(
            model_name='workshopinquiryrequest',
            name='public_event',
            field=models.CharField(blank=True, choices=[('', 'Not sure yet.'), ('invite', 'This event is open to learners by invitation only.'), ('closed', 'This event is open to learners inside of my institution.'), ('public', 'This event is open to learners outside of my institution.'), ('other', 'Other:')], default='', help_text='Many of our workshops restrict registration to learners from the hosting institution. If your workshop will be open to registrants outside of your institution please let us know below.', max_length=20, verbose_name='Is this workshop open to the public?'),
        ),
        migrations.AlterField(
            model_name='workshopinquiryrequest',
            name='travel_expences_management',
            field=models.CharField(blank=True, choices=[('', 'Not sure yet.'), ('booked', 'Hotel and airfare will be booked by site; ground travel and meals/incidentals will be reimbursed within 60 days.'), ('reimbursed', 'All expenses will be booked by instructors and reimbursed within 60 days.'), ('other', 'Other:')], default='', max_length=20, verbose_name='How will you manage travel expenses for Carpentries Instructors?'),
        ),
    ]
