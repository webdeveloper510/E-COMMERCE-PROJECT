# Generated by Django 4.1 on 2022-08-19 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0005_alter_totalprice_total_variant_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='totalprice',
            name='total_variant_price',
        ),
        migrations.AddField(
            model_name='price',
            name='total_variant_price',
            field=models.FloatField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
