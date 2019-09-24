# Generated by Django 2.2.5 on 2019-09-24 07:31

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(default='', max_length=255)),
                ('website', models.CharField(default='', max_length=255)),
                ('desc', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('group_code_canvas', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Proposals_Incoming',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='NO TITLE', max_length=255)),
                ('description', models.TextField(default='NO DESCRIPTION')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='N/A', max_length=50)),
                ('client_name', models.CharField(default='N/A', max_length=255)),
                ('company_desc', models.TextField(default='N/A')),
                ('company_website', models.CharField(default='N/A', max_length=255)),
                ('company_address', models.CharField(default='N/A', max_length=255)),
                ('contact_name', models.CharField(default='N/A', max_length=255)),
                ('contact_phone', models.CharField(default='N/A', max_length=10)),
                ('contact_email', models.CharField(default='N/A', max_length=255)),
                ('contact_position', models.CharField(default='N/A', max_length=255)),
                ('department_name', models.CharField(default='N/A', max_length=255)),
                ('department_phone', models.CharField(default='N/A', max_length=10)),
                ('department_email', models.CharField(default='N/A', max_length=255)),
                ('proposal_specialisation', models.TextField(default='N/A')),
                ('proposal_skills', models.TextField(default='N/A')),
                ('proposal_environment', models.TextField(default='N/A')),
                ('proposal_research', models.TextField(default='N/A')),
                ('supervisor_name', models.CharField(default='N/A', max_length=255)),
                ('supervisor_phone', models.CharField(default='N/A', max_length=10)),
                ('supervisor_email', models.CharField(default='N/A', max_length=255)),
                ('supervisor_title', models.CharField(default='N/A', max_length=255)),
            ],
            managers=[
                ('proposals', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Supervisors_External',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_first', models.CharField(default='', max_length=128)),
                ('name_last', models.CharField(default='', max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Supervisors_Internal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_first', models.CharField(default='', max_length=128)),
                ('name_last', models.CharField(default='', max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Units',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=128)),
                ('date_modified', models.DateField(auto_now=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('unit_code', models.CharField(default='AAA0001', max_length=8)),
                ('BB_unit_code', models.CharField(default='AAA0001', max_length=8)),
                ('ulos', models.TextField(default='')),
                ('num_students', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_first', models.CharField(default='', max_length=128)),
                ('name_last', models.CharField(default='', max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.Projects')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.Units')),
            ],
        ),
        migrations.CreateModel(
            name='Proposals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('desc', models.TextField(default='')),
                ('status', models.CharField(default='', max_length=255)),
                ('spec', models.TextField(default='')),
                ('skills', models.TextField(default='')),
                ('env', models.TextField(default='')),
                ('res', models.TextField(default='')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.Clients')),
                ('proposal_incoming', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.Proposals_Incoming')),
                ('supervisors_external', models.ManyToManyField(to='CPPMS.Supervisors_External')),
            ],
        ),
        migrations.AddField(
            model_name='projects',
            name='proposal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.Proposals'),
        ),
        migrations.AddField(
            model_name='projects',
            name='supervisors_internal',
            field=models.ManyToManyField(to='CPPMS.Supervisors_Internal'),
        ),
        migrations.AddField(
            model_name='projects',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.Units'),
        ),
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('phone', models.CharField(default='00000000', max_length=10)),
                ('email', models.CharField(default='', max_length=255)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.Companies')),
            ],
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('position', models.CharField(default='', max_length=128)),
                ('phone', models.CharField(default='00000000', max_length=10)),
                ('email', models.CharField(default='', max_length=255)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.Departments')),
            ],
        ),
        migrations.AddField(
            model_name='clients',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.Companies'),
        ),
        migrations.AddField(
            model_name='clients',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.Contacts'),
        ),
    ]
