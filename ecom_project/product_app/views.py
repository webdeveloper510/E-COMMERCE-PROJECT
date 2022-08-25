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
    queryset = Variant_type.objects.all().order_by('id')
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
        total = 0
        if request.method == 'POST':
          return Response({'msg':"success",'status':'status.HTTP_200_OK'})

        elif request.method == 'GET':
            attributes = request.data.get('attributes')
            category_id = request.data.get('category_id')
            product_id = request.data.get('product_id')
            totalprice = 0
            one_unit_price = 0
            
            for x in attributes:
                id = x['variant_type_id']
                value = x['value']

                name = Variant_type.objects.filter(id=id).values('variant_type_name', 'id')
                for x in name:
                    type_name = x['variant_type_name']
                    variant_type_id = x['id']

                if id == variant_type_id and type_name == 'picture height':
                    picture_height = value
                
                if id == variant_type_id and type_name == 'picture width':
                    picture_width = value
                    picture_size = picture_height*picture_width
                    print(picture_size)

                
                if id == variant_type_id:
                    frame_height = value
                    frame_height_feet = frame_height/12
                    print(frame_height_feet)

                if id == variant_type_id and type_name == 'frame width':
                    frame_width = value
                    frame_size = frame_height * frame_width
                    frame_width_feet = frame_width/12
                    frame_feet_size = (picture_width+(2*frame_width_feet)) * (picture_height+(2*frame_height_feet))
                    print(frame_feet_size)
                
                
                    melamine_base_price = Variant.objects.filter(variant_name='Melamine Base').values('price')
                    melamine_base_price = melamine_base_price[0]['price']
                    print(melamine_base_price)
                    melamine_base_price = frame_feet_size*melamine_base_price

                    melamine_front_price = Variant.objects.filter(variant_name='Melamine acylic front color').values('price')
                    melamine_front_price = melamine_front_price[0]['price']
                    print(melamine_front_price)
                    melamine_front_price = frame_feet_size*melamine_front_price

                    melamine_back_price = Variant.objects.filter(variant_name='Melamine acylic back color').values('price')
                    melamine_back_price = melamine_back_price[0]['price']
                    print(melamine_back_price)
                    melamine_back_price = frame_feet_size*melamine_back_price

                if picture_height <=24: 
                    stand_offs_quantity = 2
                
                elif picture_height >=25 and picture_height <=36: 
                    stand_offs_quantity = 3
                
                elif picture_height >=25 and picture_height <=36: 
                    stand_offs_quantity = 3

                elif picture_height >=37 and picture_height <=48: 
                    stand_offs_quantity = 4
                
                elif picture_height >=49 and picture_height <=60: 
                    stand_offs_quantity = 5
                
                else: 
                    print (0)
                
                stand_offs_price = Variant.objects.filter(variant_name='stand offs').values('price')
                stand_offs_price = stand_offs_price[0]['price']
                stand_offs_price = stand_offs_price * stand_offs_quantity
                print(stand_offs_price)

                
                total = melamine_base_price + melamine_front_price + melamine_back_price + stand_offs_price
                print("hii")
                print(total)

            return Response({'status':'status.HTTP_200_OK',"total":melamine_front_price})

    
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

    @action(detail=False, methods=['get'])
    def get_field_type(self, request):
        field_type = Variant._meta.get_field('variant_name').get_internal_type()
        return Response({'field_type':field_type})





# class CalculatePriceViewSet(viewsets.ViewSet):
#     @csrf_exempt 
#     @action(detail=False, methods=['post','get'])
#     def price(self, request, *args, **kwargs):
#         if request.method == 'POST':
#           return Response({'msg':"success",'status':'status.HTTP_200_OK'})

#         elif request.method == 'GET':
#             attributes = request.data.get('attributes')
#             category_id = request.data.get('category_id')
#             product_id = request.data.get('product_id')
#             totalprice = 0
#             one_unit_price = 0
#             for x in attributes:
#                 productattributes = ProductAttribute.objects.filter(category=category_id,product=product_id,variant_type_name=x["variant_type_id"]).values()
#                 one_unit_price = productattributes[0]["price"]/productattributes[0]["unit"]
#                 totalprice = totalprice + (one_unit_price*x["value"])
#             return Response({'status':'status.HTTP_200_OK',"total":totalprice})
