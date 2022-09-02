from django.db import models
from account_app.models import *

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

