# Generated by Django 2.2.8 on 2022-09-09 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='street_address',
            field=models.CharField(max_length=250),
        ),
    ]
