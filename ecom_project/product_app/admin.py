
from django.contrib import admin
from .models import *


admin.site.register(Cart)
admin.site.register(DeliveryCost)
admin.site.register(ProductAttribute)
admin.site.register(ProductVariant)

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'name')


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'name')

@admin.register(Variant_type)
class VariantsModelAdmin(admin.ModelAdmin):
  list_display = ('id','type')

@admin.register(Variant)
class CheckoutsModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'variant_type','variant_name')

@admin.register(Types)
class CheckoutsModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'variant','category','price')

@admin.register(Price)
class PriceModelAdmin(admin.ModelAdmin):
  Model = Price
  fields = ['id', 'type_id', 'value', 'total']
  list_display = ('id', 'type_id','value')


@admin.register(ProductAttribute)
class AttributeModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'variant_type','variant','price')





''' 
@admin.register(Variant_type)
class VariantsModelAdmin(admin.ModelAdmin):
  list_display = ('id','type')

@admin.register(Variant)
class CheckoutsModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'variant_type')

@admin.register(Types)
class CheckoutsModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'variant','category','price')
''' 

   
