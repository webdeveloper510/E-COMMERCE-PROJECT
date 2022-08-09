<<<<<<< HEAD
from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(DeliveryCost)
=======
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
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user','item','quantity',' created_at',' updated_at']
>>>>>>> 110fbc4aa332b711b5cc4b027c9b7f36f7b01aa1
