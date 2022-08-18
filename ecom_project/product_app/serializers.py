
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
        
    '''def to_representation(self, obj):
        return {
            "category": obj.category.name,
            "category_id": obj.category.id,
            "name": obj.name,
            "description": obj.description,
            "price": obj.price,
            "length": obj.length,
            "width": obj.width,
            "depth": obj.depth,
            "paper": obj.paper,
            "coating": obj.coating,
            "printed_sides": obj.printed_sides,
            "quantity": obj.quantity,
         }
    
  '''
    def create(self, validate_data):
     return Product.objects.create(**validate_data)
''' 
class Variant_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant_type
        fields = "__all__"

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = "__all__"

class TypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = "__all__"
 ''' 
class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = "__all__"
        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields="__all__"

    def create(self, validate_data):
     return Cart.objects.create(**validate_data)    

class DeliveryCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryCost
        fields = ['id', 'cost_per_delivery', 'cost_per_product', 'fixed_cost']


class Variant_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant_type
        fields = "__all__"

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = "__all__"

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProductAttribute
        fields="__all__"

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields="__all__"


class TypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Types
        fields = "__all__"

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['id', 'type_id', 'value']
