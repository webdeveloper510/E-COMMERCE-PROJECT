# Generated by Django 4.0.5 on 2022-08-03 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='tc',
        ),
    ]