# Generated by Django 2.2.5 on 2019-09-30 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CPPMS', '0004_auto_20190930_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
