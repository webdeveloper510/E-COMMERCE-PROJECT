
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
        fields="__all__"
    '''
    def to_representation(self, obj):
        return {
             "category": obj.category.name,
             "descrption":obj.description,
             "image":obj.description,
        }
      '''  
  
    def create(self, validate_data):
     return Product.objects.create(**validate_data)
 
class Variant_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model= Variant_type
        fields="__all__"

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model= Variant
        fields="__all__"

        def to_representation(self, obj):
         return {
             "variant_id": obj.id,
             "variant_type":obj.variant_type.type,
             "variant_type_id":obj.variant_type.id,
             "category_id":obj.category.id,
             "price":obj.price,
         }

         

class TypesSerializer(serializers.ModelSerializer):
    class Meta:
        model= Types
        fields="__all__"

        def to_representation(self, obj):
         return {
             "variant_id": obj.variant.id,
             "category_id":obj.category.id,
             "price":obj.price,
         }

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

