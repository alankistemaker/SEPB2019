# Generated by Django 2.2.5 on 2019-10-12 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CPPMS', '0006_auto_20191012_1200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='name_first',
        ),
        migrations.RemoveField(
            model_name='student',
            name='name_last',
        ),
        migrations.AddField(
            model_name='student',
            name='name',
            field=models.CharField(default='', max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(default='', max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(default='', max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(default='', max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(default='', max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(default='', max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='title',
            field=models.CharField(default='', max_length=128, unique=True),
        ),
    ]
