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

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = "__all__"

        def to_representation(self, obj):
         return {
            "variant_name": obj.variant_name,
            "variant_Type": obj.type.name,
            "variant_price":obj.price
                       }   

class Variant_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant_type
        fields = "__all__"

    def to_representation(self, obj):
        return {
            "variant_type_id": obj.id,
            "variant_id": obj.variant.id,
            "variant_name": obj.variant.variant_name,
            "variant_type_name":obj.variant_type_name,
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


class HeightSerializer(serializers.ModelSerializer):
    class Meta:
        model= Height
        fields="__all__"

        def to_representation(self, obj):
         return {
            "id": obj.id,
            "unit_mm": obj.unit_mm,
            "price": obj.price,
            "variant_name": obj.variant.variant_name,
          }   

class WidthSerializer(serializers.ModelSerializer):
    class Meta:
        model= Width
        fields="__all__"

class TypeSerializer(serializers.ModelSerializer):
        class Meta:
            model= Type
            fields = "__all__"

        def to_representation(self, obj):
         return {
            "id": obj.id,
            "variant_type": obj.variant_type.variant_name,
            "field_type": obj.field_type
          }   

