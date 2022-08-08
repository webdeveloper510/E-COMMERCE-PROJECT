from django.db import models
from django.conf import settings
from django.db import models
from django.shortcuts import reverse

class Category(models.Model):
      name = models.CharField(max_length=250)
  
      def _str_(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=500, null=False, blank= False)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    price = models.FloatField(null=False, blank= False, default=30.30)
    length = models.DecimalField(default=30.30, max_digits=5, decimal_places=1)
    width = models.DecimalField(default=30.30, max_digits=5, decimal_places=1)
    depth = models.DecimalField(default=30.30, max_digits=5, decimal_places=1)
    paper = models.CharField(max_length=90)
    coating = models.CharField(max_length=90)
    printed_sides = models.CharField(max_length=90)
    quantity = models.IntegerField(default=1)

    def _str_(self):
     return self.name
     
