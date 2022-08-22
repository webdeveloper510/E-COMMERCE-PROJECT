
from django.contrib import admin
from .models import *


admin.site.register(ProductAttribute)
admin.site.register(Order)
admin.site.register(OrderItem)

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

@admin.register(Price)
class PriceModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'type_id','value','variant_price')

@admin.register(Totalprice)
class TotalpriceModelAdmin(admin.ModelAdmin):
  Model = Totalprice
  list_display = ('id', 'cost_per_delivery','cost_per_product','tax','total_cost')

'''
@admin.register(Types)
class TypesModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'variant','category','price')
'''
