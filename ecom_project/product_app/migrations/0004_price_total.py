# Generated by Django 4.1 on 2022-08-18 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0003_remove_cart_created_at_remove_cart_item_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='total',
            field=models.FloatField(default=1, verbose_name='total'),
            preserve_default=False,
        ),
    ]
