# Generated by Django 2.2.5 on 2019-10-11 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CPPMS', '0002_project_completed'),
    ]

    operations = [
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
        migrations.RemoveField(
            model_name='client',
            name='company',
        ),
        migrations.RemoveField(
            model_name='department',
            name='company',
        ),
        migrations.AddField(
            model_name='client',
            name='address',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='client',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.Department'),
        ),
        migrations.AddField(
            model_name='client',
            name='desc',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='client',
            name='website',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]