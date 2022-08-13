
from django.db import models
from account_app.models import *
import datetime
from django.conf import settings
from django.db import models

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
    
class Variant_type(models.Model):
        type = models.CharField(max_length=250)

        def __str__(self):
          return (self.type)
        
class Variant(models.Model):
        name = models.CharField(max_length=250)
        variant_type = models.ForeignKey(Variant_type, on_delete=models.CASCADE)

        def __str__(self):
          return (self.name)


class Types(models.Model):
        variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)
        price = models.CharField(max_length=50)

        def __str__(self):
          return (self.price)
    

class ProductAttribute(models.Model):
  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attr_type = models.ForeignKey(Variant_type, on_delete=models.PROTECT, blank=True, null=True)
    attr_name = models.CharField(max_length=155, blank=True)


class ProductVariant(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ManyToManyField(ProductAttribute)
    price = models.DecimalField(max_digits=25, decimal_places=2)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.ForeignKey(Types, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.user,
                                               self.category,
                                               self.product,
                                               self.type,
                                               self.quantity,
                                               self.created_at,
                                               self.updated_at)

class DeliveryCost(models.Model):
    status = models.CharField(max_length=7,
                              choices=(('Active', 'active'), ('Passive', 'passive')),
                              default="passive",
                              null=False)
    cost_per_delivery = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    cost_per_product = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    fixed_cost = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {} - {} - {}".format(self.status,
                                                    self.cost_per_delivery,
                                                    self.cost_per_product,
                                                    self.fixed_cost,
                                                    self.created_at,
                                                    self.updated_at)

