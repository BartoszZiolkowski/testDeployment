# Generated by Django 2.1.1 on 2018-09-24 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20180910_2024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sample',
            name='barcode',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='photo',
        ),
    ]
