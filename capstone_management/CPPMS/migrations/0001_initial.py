# Generated by Django 2.2.5 on 2019-10-13 05:22

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Archive_Proposal',
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
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(default='', max_length=255)),
                ('website', models.CharField(default='', max_length=255)),
                ('desc', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('phone', models.CharField(default='00000000', max_length=10)),
                ('email', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='External_Supervisor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.CharField(default='', max_length=255)),
                ('phone', models.CharField(default='00000000', max_length=10)),
                ('title', models.CharField(default='N/A', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('group_code_canvas', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Incoming_Proposal',
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
            name='Internal_Supervisor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.CharField(default='', max_length=255)),
                ('phone', models.CharField(default='00000000', max_length=10)),
                ('title', models.CharField(default='N/A', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.CharField(default='', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=128, unique=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('unit_code', models.CharField(default='AAA0001', max_length=8)),
                ('BB_unit_code', models.CharField(default='AAA0001', max_length=8)),
                ('ulos', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Upload_Proposal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=128)),
                ('filepath', models.FileField(blank=True, default='', null=True, upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proposal',
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
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CPPMS.Client')),
                ('proposal_incoming', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.Incoming_Proposal')),
                ('supervisors_external', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.External_Supervisor')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=128, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(default='', max_length=128)),
                ('year', models.IntegerField(default='0000')),
                ('completed', models.BooleanField(default=0)),
                ('group_members', models.ManyToManyField(through='CPPMS.Group', to='CPPMS.Student')),
                ('internal_supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.Internal_Supervisor')),
                ('proposal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CPPMS.Proposal')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.Unit')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_leader', to='CPPMS.Student'),
        ),
        migrations.AddField(
            model_name='group',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.Project'),
        ),
        migrations.AddField(
            model_name='group',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.Student'),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('position', models.CharField(default='', max_length=128)),
                ('phone', models.CharField(default='00000000', max_length=10)),
                ('email', models.CharField(default='', max_length=255)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.Department')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.Contact'),
        ),
        migrations.AddField(
            model_name='client',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.Department'),
        ),
    ]
