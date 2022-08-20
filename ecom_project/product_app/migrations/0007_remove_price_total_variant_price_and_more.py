# Generated by Django 4.1 on 2022-08-19 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0006_remove_totalprice_total_variant_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='price',
            name='total_variant_price',
        ),
        migrations.AddField(
            model_name='totalprice',
            name='total_variant_price',
            field=models.FloatField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
