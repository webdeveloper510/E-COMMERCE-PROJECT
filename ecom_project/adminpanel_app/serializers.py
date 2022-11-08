from rest_framework import serializers
from .models import *

class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logo
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

class FAQSerializer(serializers.ModelSerializer):
     class Meta:
        model= FAQ
        fields = '__all__'
 
  