# Generated by Django 3.1.7 on 2021-03-10 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_order_orderproduct'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderproduct',
            old_name='quatity',
            new_name='quantity',
        ),
    ]
