# Generated by Django 2.2.8 on 2022-08-25 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='variant',
            name='ft',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='variant',
            name='price',
            field=models.FloatField(default=100),
        ),
    ]
