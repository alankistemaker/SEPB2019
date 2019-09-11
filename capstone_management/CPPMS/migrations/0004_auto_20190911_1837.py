# Generated by Django 2.2.5 on 2019-09-11 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CPPMS', '0003_auto_20190911_1709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposals_incoming',
            name='name',
        ),
        migrations.RemoveField(
            model_name='units',
            name='supervisors',
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='client_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='company_address',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='company_desc',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='company_website',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='contact_email',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='contact_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='contact_phone',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='contact_position',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='department_email',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='department_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='department_phone',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='proposal_environment',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='proposal_research',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='proposal_skills',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='proposal_specialisation',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='status',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='supervisor_email',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='supervisor_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='supervisor_phone',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='supervisor_title',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='proposals_incoming',
            name='title',
            field=models.CharField(default='NO TITLE', max_length=255),
        ),
    ]
