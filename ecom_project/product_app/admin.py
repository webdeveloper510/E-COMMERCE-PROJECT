from django.contrib import admin
from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','category','name','description','image','price',
    'length','width','depth','paper','coating','printed_sides','quantity']

@admin.register(Cart)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','user','item','quantity','created_at','updated_at']

@admin.register(DeliveryCost)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['status']
