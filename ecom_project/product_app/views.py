from unicodedata import category
from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
#from product_app.helper import *
from django.views.decorators.csrf import csrf_exempt

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('category_id')
    serializer_class = ProductSerializer

class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variant.objects.all().order_by('id')
    serializer_class = VariantSerializer

class Variant_typeViewSet(viewsets.ModelViewSet):
    queryset = Variant_type.objects.filter(variant_id=2).order_by('id')
    serializer_class = Variant_typeSerializer
    
class ProductAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductAttribute.objects.all().order_by('id')
    serializer_class = ProductAttributeSerializer
    
class HeightViewSet(viewsets.ModelViewSet):
    queryset = Height.objects.all().order_by('id')
    serializer_class = HeightSerializer
    
class WidthViewSet(viewsets.ModelViewSet):
    queryset = Width.objects.all().order_by('id')
    serializer_class = WidthSerializer
    
class CalculatePriceViewSet(viewsets.ViewSet):
    @csrf_exempt 
    @action(detail=False, methods=['post','get'])
    def price(self, request, *args, **kwargs):
        if request.method == 'POST':
          return Response({'msg':"success",'status':'status.HTTP_200_OK'})

        elif request.method == 'GET':
            attributes = request.data.get('attributes')
            category_id = request.data.get('category_id')
            product_id = request.data.get('product_id')
            totalprice = 0
            oneunitprice = 0
            for x in attributes:
                productattributes = ProductAttribute.objects.filter(category=category_id,product=product_id,variant_type_name=x["variant_type_id"]).values()
                oneunitprice = productattributes[0]["price"]/productattributes[0]["unit"]
                totalprice = totalprice + (oneunitprice*x["value"])
            return Response({'status':'status.HTTP_200_OK',"total":totalprice})


class Variant_type_list_ViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get','post'])
    def types(self, request, *args, **kwargs):
        variant_name = request.data.get('variant_name')
        variant = Variant.objects.get(variant_name=variant_name)
        list = Variant_type.objects.filter(variant=variant).values('variant_type_name','id')
        attributes = ProductAttribute.objects.all().values('category_id','product_id','variant_type_name_id')
        return Response({'Variant_name':variant_name,"product_attributes":attributes,"Variant_type_list":list})
       
class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all().order_by('id')
    serializer_class = TypeSerializer

    