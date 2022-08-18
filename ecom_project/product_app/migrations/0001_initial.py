# Generated by Django 4.1 on 2022-08-17 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Active', 'active'), ('Passive', 'passive')], default='passive', max_length=7)),
                ('cost_per_delivery', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cost_per_product', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fixed_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(max_length=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=25)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.product')),
            ],
        ),
        migrations.CreateModel(
            name='Variant_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_name', models.CharField(max_length=250)),
                ('variant_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.variant_type')),
            ],
        ),
        migrations.CreateModel(
            name='Types',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.category')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.variant')),
            ],
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=25)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.product')),
                ('variant', models.ManyToManyField(to='product_app.productattribute')),
            ],
        ),
        migrations.AddField(
            model_name='productattribute',
            name='variant_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.variant'),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='variant_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='product_app.variant_type'),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product_app.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
