# Generated by Django 3.1.7 on 2021-03-06 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210306_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productflavor',
            name='stock',
        ),
    ]
