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

  def has_add_permission(self, request):
    return False

  def has_delete_permission(self, request, obj=None):
    return False

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
  list_display = ('id','product','item','status','quantity','user_id','name','email','contact','street_address','apartment',
  'zip_code','state','city','total')

@admin.register(Shipping)
class ShippingModelAdmin(admin.ModelAdmin):
  list_display = ('id','percentage')

@admin.register(Frame_Image)
class Frame_ImageModelAdmin(admin.ModelAdmin):
  list_display = ('id','image','user_id','order_id')