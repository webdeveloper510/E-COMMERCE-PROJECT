
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

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields="__all__"

    def create(self, validate_data):
     return Cart.objects.create(**validate_data)    

class DeliveryCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryCost
        fields = ['id', 'status', 'cost_per_delivery', 'cost_per_product', 'fixed_cost', 'created_at', 'updated_at']

