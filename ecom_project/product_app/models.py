from django.db import models
from account_app.models import *
import datetime
from ecom_project import settings
from django.db.models import F, Sum
from rest_framework.response import Response
from django import forms

class Category(models.Model):
      name = models.CharField(max_length=250)
  
      def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=500, null=False, blank= False)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Variant(models.Model):
        variant_name = models.CharField(max_length=250)
       
        def __str__(self):
         return "{} -".format(self.variant_name)

# type_choices = [
#     ('Coating', ( ('coating 1','coating 1'),('coating 2','coating 2') )),
#     ('Paper', ( ('glossy', 'glossy'),('cardstock','cardstock') ) ),
#     ('Printed Sides', ( ('all', 'all'), ('inside','inside') ) ),
# ]
class Variant_type(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    variant_type_name = models.CharField(max_length = 90 )

    def __str__(self):
         return "{} - {} -".format(self.variant, self.variant_type_name)
        
class ProductAttribute(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant_type_name = models.ForeignKey(Variant_type, on_delete=models.CASCADE)
    unit = models.FloatField(default=1.0)
    price = models.FloatField(default=100)

    def __str__(self):
        return "{} - {} -".format(self.category,self.product,self.variant_type_name,
                                    self.unit, self.price)


class Height(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    price = models.FloatField(default=100)
    unit_mm = models.FloatField(default=100)

    def __str__(self):
         return "{} - {} -".format(self.variant, self.price,self.unit_mm)
        

class Width(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    price = models.FloatField(default=100)
    unit_mm = models.FloatField(default=100)

    def __str__(self):
         return "{} - {} -".format(self.variant, self.price,self.unit_mm)
        
class Type(models.Model):
    # type = models.ManyToManyField(Variant_type)
    type = models.ForeignKey(Variant_type, on_delete=models.CASCADE)
    status = models.BooleanField()

    def __str__(self):
        return "{}-{}".format(self.type,self.status)
