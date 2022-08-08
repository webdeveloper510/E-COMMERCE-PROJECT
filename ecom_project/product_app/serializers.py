from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
     class Meta:
        model= Category
        fields = '__all__'
           
     def create(self, validate_data):
        #print(validate_data)
        return Category.objects.create(**validate_data)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields = '__all__'
  
    def create(self, validate_data):
     return Product.objects.create(**validate_data)

     

