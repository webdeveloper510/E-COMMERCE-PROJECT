# Generated by Django 4.1 on 2022-08-18 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0011_alter_price_variant_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='total_variant_price',
            field=models.CharField(max_length=90, null=True),
        ),
    ]
