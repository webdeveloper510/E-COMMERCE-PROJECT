from unicodedata import category
from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
#from product_app.helper import *
from django.views.decorators.csrf import csrf_exempt
from distutils import errors
from django.shortcuts import get_object_or_404

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
    queryset = Variant_type.objects.all().order_by('id')
    serializer_class = Variant_typeSerializer
    
class ProductAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductAttribute.objects.all().order_by('id')
    serializer_class = ProductAttributeSerializer
    
class ElementsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Elements.objects.all().order_by('id')
    serializer_class = ElementsSerializer
    
class WidthViewSet(viewsets.ModelViewSet):
    queryset = Width.objects.all().order_by('id')
    serializer_class = WidthSerializer

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

class Send_listViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post','get'])
    def dict(self, request, *args, **kwargs):
        queryset = Variant.objects.all().values('variant_name','field_type')
        serializer_class = VariantSerializer
        types = Variant_type.objects.all().values('variant_type_name')
        serializer_class = VariantSerializer

        dropdown = Variant.objects.all().values('id','variant_name','field_type') 
        array = []
        for x in dropdown:
            variant_id = x['id']
            variant_name= x['variant_name']
            field_Type = x['field_type']
            dropdown_options = Variant_type.objects.filter(variant=variant_id).values('id','variant_type_name')
            queryset = {'Field Type':field_Type,'Title':variant_name,'variant_id':variant_id,'options':dropdown_options}
            array.append(queryset)
        return Response({'list':array})


class CalculatePriceViewSet(viewsets.ViewSet):
    back_price = ""
    @csrf_exempt 
    @action(detail=False, methods=['post','get'])
    def price(self, request, *args, **kwargs):
        if request.method == 'POST':
            attributes = request.data.get('attributes')
            category_id = request.data.get('category_id')
            product_id = request.data.get('product_id')
            frame_feet_size = 0
            frame_height = 0
            frame_height_feet = 0
            for x in attributes:
                id = x['variant_type_id']
                value = x['value']

                name = Variant_type.objects.filter(id=id).values('variant_type_name', 'variant_id','id','variant','variant__variant_name','variant__element','variant__element__element')
                
                if id == name[0]['id'] and name[0]['variant__element__element']  == 'Picture height':
                    picture_height = value

                if id == name[0]['id'] and name[0]['variant__element__element']  == 'Picture width':
                    picture_width = value

                if id == name[0]['id'] and name[0]['variant__element__element'] == 'Frame height':
                    frame_height = value
                           
                if id == name[0]['id'] and name[0]['variant__element__element']  == 'Frame width':
                    frame_width = value
                    frame_feet_size = (picture_height+(2 * frame_height)) * ((picture_width + (2 * frame_width))) /12

                if id == name[0]['id'] and name[0]['variant__element__element']  == 'Base color':
                    b__price = ProductAttribute.objects.filter(variant_type_name_id=name[0]['id']).values('price')
                    base_price = frame_feet_size * b__price[0]['price']

                if id == name[0]['id'] and name[0]['variant__element__element']  == 'Front color':
                    f_price = ProductAttribute.objects.filter(variant_type_name_id=name[0]['id']).values('price')
                    front_price = frame_feet_size * f_price[0]['price']
                
                if id == name[0]['id'] and name[0]['variant__element__element']  == 'Back color':
                    bck_price = ProductAttribute.objects.filter(variant_type_name_id=name[0]['id']).values('price')
                    back_price = frame_feet_size * bck_price[0]['price']

                if picture_width >=0 and picture_width <=24: 
                    stand_offs_quantity = 2 + 2
                
                if picture_width >=25 and picture_width <=36: 
                    stand_offs_quantity = 3 + 3
                
                if picture_width >=37 and picture_width <=48: 
                    stand_offs_quantity = 4 + 4
                
                if picture_width >=49 and picture_width <=60: 
                    stand_offs_quantity = 5 + 5 
                    
                if id == name[0]['id'] and name[0]['variant__element__element']  == 'Stand off':
                    s_price = ProductAttribute.objects.filter(variant_type_name_id=name[0]['id']).values('price')
                    stand_offs_price = stand_offs_quantity * s_price[0]['price']
                    
            total = base_price + front_price + back_price + stand_offs_price
   
            return Response({'status':'status.HTTP_200_OK',"picture_height": picture_height,
             "picture_width":picture_width,"frame_height":frame_height,"frame_width":frame_width,
             "frame_feet_size":frame_feet_size, "base_price":(b__price[0]['price'],base_price),
             "front_price":(f_price[0]['price'],front_price),"back_price":(bck_price[0]['price'],back_price),
             "stand_offs_quantity":stand_offs_quantity,"stand_offs_price":(s_price[0]['price'],stand_offs_price),
             "total":total,
            })

                  
            