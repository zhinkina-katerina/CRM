# Generated by Django 3.2.9 on 2021-11-15 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0004_auto_20211115_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfromorder',
            name='quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
