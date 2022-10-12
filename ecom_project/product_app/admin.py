
from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'name')

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
  list_display = ('id', 'name')

@admin.register(Elements)
class ElementsModelAdmin(admin.ModelAdmin):
  list_display = ('id','element')

@admin.register(Variant)
class VariantModelAdmin(admin.ModelAdmin):
  list_display = ('id','element','variant_name','field_type')

@admin.register(Variant_type)
class Variant_typeModelAdmin(admin.ModelAdmin):
  list_display = ('id','variant','variant_type_name')

@admin.register(ProductAttribute)
class ProductAttributeModelAdmin(admin.ModelAdmin):
  list_display = ('id','category','product','variant_type_name','unit','price')

@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
  list_display = ('id','item','status','quantity','user_id','name','email','contact','street_address','apartment',
  'zip_code','state','city','total')

@admin.register(Shipping)
class ShippingModelAdmin(admin.ModelAdmin):
  list_display = ('id','percentage')

@admin.register(Order_item)
class Order_itemModelAdmin(admin.ModelAdmin):
  list_display = ('id','user','item','product_name','status')
