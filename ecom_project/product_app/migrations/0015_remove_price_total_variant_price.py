# Generated by Django 4.1 on 2022-08-18 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0014_alter_price_total_variant_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='price',
            name='total_variant_price',
        ),
    ]
