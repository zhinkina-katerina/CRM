# Generated by Django 3.2.9 on 2022-01-11 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0009_order_total_price'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductFromOrder',
            new_name='Product',
        ),
    ]
