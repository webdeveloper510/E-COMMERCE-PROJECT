from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseCategoryAdmin


admin.site.register(Cart)
admin.site.register(DeliveryCost)
admin.site.register(ProductVariant)
admin.site.register(ProductAttribute)

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'name')


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'name')

@admin.register(Variant_type)
class Variant_typeModelAdmin(admin.ModelAdmin):
  list_display = ('id','type')

@admin.register(Variant)
class VariantModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'variant_type')

@admin.register(Types)
class TypesModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'variant','category','price')