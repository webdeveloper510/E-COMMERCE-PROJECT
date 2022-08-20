from django.contrib import admin
from .models import *


admin.site.register(Cart)
admin.site.register(ProductAttribute)
admin.site.register(ProductVariant)

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
  list_display = ('id', 'variant_type','variant_name')

@admin.register(Types)
class TypesModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'variant','category','price')

@admin.register(Price)
class PriceModelAdmin(admin.ModelAdmin):
  Model = Price
  #fields = ['id', 'type_id', 'value', 'variant_price']
  list_display = ('id', 'type_id','value','variant_price')


# @admin.register(Total_Price)
# class Total_PriceModelAdmin(admin.ModelAdmin):
#   Model = Total_Price
#   list_display = ('id', 'cost_per_delivery','cost_per_product','tax','total_cost')