
from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'name')

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'name')

@admin.register(Variant)
class VariantModelAdmin(admin.ModelAdmin):
  list_display = ('id','variant_name','price')

@admin.register(Variant_type)
class Variant_typeModelAdmin(admin.ModelAdmin):
  list_display = ('id','variant','variant_type_name')

@admin.register(ProductAttribute)
class ProductAttributeModelAdmin(admin.ModelAdmin):
  list_display = ('id','category','product','variant_type_name','unit','price')

@admin.register(Height)
class PriceModelAdmin(admin.ModelAdmin):
  list_display = ('id','variant','price','unit_mm')

@admin.register(Width)
class PriceModelAdmin(admin.ModelAdmin):
  list_display = ('id','variant','price','unit_mm')

@admin.register(Type)
class TypeModelAdmin(admin.ModelAdmin):
  list_display = ('id','variant_type','field_type')

