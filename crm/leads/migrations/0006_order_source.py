# Generated by Django 3.2.9 on 2021-11-16 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0005_productfromorder_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='source',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
    ]