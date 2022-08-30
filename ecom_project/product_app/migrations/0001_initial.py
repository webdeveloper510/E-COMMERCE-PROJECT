# Generated by Django 2.2.8 on 2022-08-25 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(max_length=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Width',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=100)),
                ('unit_mm', models.FloatField(default=100)),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.Variant')),
            ],
        ),
        migrations.CreateModel(
            name='Variant_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_type_name', models.CharField(max_length=90)),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.Variant')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_type', models.CharField(choices=[('dropdown', 'dropdown'), ('checkbox', 'checkbox'), ('inputbox', 'inputbox'), ('Charfield', 'charfield'), ('Foriegnkey', 'foriegnkey'), ('integerfield', 'integerfield')], default='select', max_length=90)),
                ('variant_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.Variant')),
            ],
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.FloatField(default=1.0)),
                ('price', models.FloatField(default=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.Category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.Product')),
                ('variant_type_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.Variant_type')),
            ],
        ),
        migrations.CreateModel(
            name='Height',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=100)),
                ('unit_mm', models.FloatField(default=100)),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.Variant')),
            ],
        ),
    ]
