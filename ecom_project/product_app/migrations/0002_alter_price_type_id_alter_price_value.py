# Generated by Django 4.1 on 2022-08-19 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='type_id',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='price',
            name='value',
            field=models.FloatField(null=True),
        ),
    ]
