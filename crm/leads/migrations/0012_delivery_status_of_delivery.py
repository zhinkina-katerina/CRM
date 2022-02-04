# Generated by Django 3.2.9 on 2022-01-29 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0011_rename_product_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='status_of_delivery',
            field=models.CharField(choices=[('New', 'Новый'), ('In_process', 'В процессе'), ('Done', 'Выполнен'), ('Canceled', 'Отменен')], default='New', max_length=200),
            preserve_default=False,
        ),
    ]
