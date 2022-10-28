from rest_framework import serializers
from .models import *

class LogoSerializer(serializers.ModelSerializer):
     class Meta:
        model= Logo
        fields = '__all__'
           
class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Header
        fields = "__all__"

class BannerSerializer(serializers.ModelSerializer):
     class Meta:
        model= Banner
        fields = '__all__'
           
class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = "__all__"

class CarouselSerializer(serializers.ModelSerializer):
     class Meta:
        model= Carousel
        fields = '__all__'
           
class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = "__all__"

class HeadingcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadingCategory
        fields = "__all__"

class HeadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Headings
        fields = "__all__"