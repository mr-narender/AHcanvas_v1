# Generated by Django 3.2 on 2022-08-05 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20220805_0320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(default='', max_length=254),
        ),
    ]
