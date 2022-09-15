from django.db import models
from account_app.models import *
import datetime

class Category(models.Model):
      name = models.CharField(max_length=250)
  
      def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=500, null=False, blank= False)
    
    def __str__(self):
        return self.name

class Elements(models.Model):
    element = models.CharField(max_length=250)

    def __str__(self):
         return "{}".format(self.element)
        
class Variant(models.Model):
        element = models.ForeignKey(Elements, on_delete=models.CASCADE)
        variant_name = models.CharField(max_length=250)
        field_type = models.CharField(max_length=250)
        def __str__(self):
         return "{} -{}".format(self.variant_name,self.element)

class Variant_type(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    variant_type_name = models.CharField(max_length = 90 )

    def __str__(self):
         return "{} - {} -".format(self.variant, self.variant_type_name)
        
class ProductAttribute(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant_type_name = models.ForeignKey(Variant_type, on_delete=models.CASCADE)
    unit = models.FloatField(default=0)
    price = models.FloatField(default=0)

    def __str__(self):
        return "{} - {} -".format(self.category,self.product,self.variant_type_name,
                                    self.unit, self.price)

class Order(models.Model):
    user_id = models.CharField(max_length=200)
    item = models.TextField(max_length=500)
    quantity = models.IntegerField()
    name = models.CharField(max_length = 250)
    email = models.EmailField()
    contact = models.CharField(max_length=30)
    street_address = models.CharField(max_length=250)
    apartment = models.CharField(max_length=250)
    zip_code = models.IntegerField(blank=True)
    state =  models.CharField(max_length=250)
    city =  models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total = models.FloatField(default=0.0)
    def __str__(self):
         return "{} -{}-{}-{}-{}-{} ".format(self.user_id,self.item,self.quantity,self.name,
                                             self.email,self.contact,self.street_address,
                                             self.apartment,self.zip_code,self.state,self.city,
                                              self.created_at,self.updated_at, self.total)
        
class Shipping(models.Model):
    percentage = models.FloatField(default=0)
      
    def __str__(self):
        return "{} - {} -".format(self.percentage)
