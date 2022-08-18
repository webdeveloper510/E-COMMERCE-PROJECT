# Generated by Django 4.0.5 on 2022-08-13 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0003_types_variant_variant_type_delete_variants_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_type', models.CharField(max_length=250)),
                ('variant', models.CharField(max_length=250)),
                ('price', models.CharField(max_length=240)),
            ],
        ),
        migrations.RemoveField(
            model_name='variant',
            name='variant_type',
        ),
        migrations.DeleteModel(
            name='Types',
        ),
        migrations.DeleteModel(
            name='Variant',
        ),
        migrations.DeleteModel(
            name='Variant_type',
        ),
    ]
