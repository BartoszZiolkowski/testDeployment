# Generated by Django 2.1.1 on 2018-09-04 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20180904_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='photo',
            field=models.ImageField(upload_to='media/'),
        ),
    ]
