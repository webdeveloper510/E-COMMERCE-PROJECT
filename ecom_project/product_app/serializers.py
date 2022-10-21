from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
     class Meta:
        model= Category
        fields = '__all__'
           
     def create(self, validate_data):
         return Category.objects.create(**validate_data)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields = '__all__'
        
    def create(self, validate_data):
     return Product.objects.create(**validate_data)

class ElementsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Elements
        fields="__all__"

        def to_representation(self, obj):
         return {
            "id": obj.id,
            "element": obj.element,
          }   

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = "__all__"

        def to_representation(self, obj):
         return {
            "element_id":obj.element.id,
            "element":obj.element.element,
            "variant_id": obj.id,
            "variant_name": obj.variant_name,
               }   

class Variant_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant_type
        fields = "__all__"

    def to_representation(self, obj):
        return {
            "variant_id": obj.variant.id,
            "variant_name": obj.variant.variant_name,
            "element_id":obj.variant.element.id,
            "variant_type_id": obj.id,
            "variant_type_name":obj.variant_type_name,
            "field_type":obj.variant.field_type
             }   

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProductAttribute
        fields="__all__"

    def to_representation(self, obj):
        return {
            "id": obj.id,
            "category_id": obj.category.id,
            "category_name": obj.category.name,
            "product_id": obj.product.id,
            "product_name": obj.product.name,
            "variant_type_id": obj.variant_type_name.id,
            "variant_type_name": obj.variant_type_name.variant_type_name,
            "price":obj.price,
            "unit":obj.unit,
             }   

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model= Order
        fields="__all__"

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model= Shipping
        fields="__all__"



