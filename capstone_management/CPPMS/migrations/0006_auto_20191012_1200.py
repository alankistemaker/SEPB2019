# Generated by Django 2.2.5 on 2019-10-12 01:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CPPMS', '0005_auto_20191012_0317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='supervisors_external',
        ),
        migrations.AddField(
            model_name='proposal',
            name='supervisors_external',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CPPMS.External_Supervisor'),
        ),
    ]