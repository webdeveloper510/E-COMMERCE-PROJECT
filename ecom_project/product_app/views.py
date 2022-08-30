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
    
class ElementsViewSet(viewsets.ModelViewSet):
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
    @csrf_exempt 
    @action(detail=False, methods=['post','get'])
    def price(self, request, *args, **kwargs):
        # if request.method == 'POST':
        #    return Response({'msg':"success",'status':'status.HTTP_200_OK'})
    
        if request.method == 'POST':
            attributes = request.data.get('attributes')
            category_id = request.data.get('category_id')
            product_id = request.data.get('product_id')
            frame_feet_size = 0
            frame_height = 0
            frame_height_feet = 0
            for x in attributes:
                e_id = x['element_id']
                id = x['variant_type_id']
                value = x['value']
                name = Variant_type.objects.filter(id=id).values('variant_type_name', 'id','variant','variant__variant_name','variant__element','variant__element__element')
                print(name[0]['variant__element'])
                # for n in name:
                #     v_t_id = n['id']
                #     element_id = n['variant__element'] 

                if id == name[0]['id'] and name[0]['variant__element'] == e_id:
                    picture_height = value
                    print("picture height --", picture_height)
                
                if id == name[0]['id'] and name[0]['variant__element'] == e_id:
                    picture_width = value
                    picture_size = picture_height * picture_width
                    picture_size_feet = picture_size / 12

                    print("picture_width ----", picture_width)
                    print("picture_size---- ", picture_size)
                    

                # if id == n['id'] and n['variant__element'] == e_id:  
                #     picture_height = value
                #     print("picture height ----",picture_height)

                # elif id == n['id'] and n['variant__element'] == e_id:  
                #     picture_width = value
                #     picture_size = picture_height * picture_width
                #     picture_size_feet = picture_size / 12
                #     print("picture_width ----",picture_width)
                #     print("picture_size ----",picture_size)

                # else:
                #     print(000000000000000000000000)

                #     print("picture height "+ str(picture_height))
                #     print("picture_width "+ str(picture_width))
                #     print("picture_size "+ str(picture_size))
                 
                # if id == variant_type_id and element_id == e_id:
                #     frame_height = value
                           
                # if id == variant_type_id and element_id == e_id:
                #     frame_width = value
                #     frame_size = frame_height * frame_width

                #     frame_height_size = (picture_height+(2*frame_height))
                #     frame_height_feet_size = frame_height_size / 12

                #     frame_width_size = (picture_width+(2*frame_width)) 
                #     frame_width_feet_size = frame_width_size / 12
                     
                #     frame_feet_size = frame_height_feet_size * frame_width_feet_size
                    
                #     print("frame_height "+ str(frame_height))
                #     print("frame_height_feet "+ str(frame_height_feet))
                #     print("frame_width "+ str(frame_width))
                #     print("frame_size "+ str(frame_size))
                #     print("frame_feet_size "+ str(frame_feet_size))
                
                # if id == variant_type_id and element_id == 1:
                #     melamine_base_price = ProductAttribute.objects.filter(variant_type_name_id=id).values('price')
                #     print("melamine price per : " + str(melamine_base_price))
                #     melamine_base_price = melamine_base_price[0]['price']
                #     melamine_base_price = frame_feet_size*melamine_base_price
                #     print("final melamine price is : " + str(melamine_base_price))

                # if id == variant_type_id and element_id == 1:
                #     melamine_front_price = ProductAttribute.objects.filter(variant_type_name_id=id).values('price')
                #     melamine_front_price = melamine_front_price[0]['price']
                #     print("melamine_front_price : "+ str(melamine_front_price))
                #     melamine_front_price = frame_feet_size*melamine_front_price

                # if id == variant_type_id and element_id == 1:
                #     melamine_back_price = ProductAttribute.objects.filter(variant_type_name_id=id).values('price')
                #     melamine_back_price = melamine_back_price[0]['price']
                #     print(melamine_back_price)
                #     melamine_back_price = frame_feet_size*melamine_back_price

                #     print("melamine_base_price "+ str(melamine_base_price))
                #     print("melamine_front_price "+ str(melamine_front_price))
                #     print("melamine_back_price "+ str(melamine_back_price))
                
                #     if picture_width >=0 and picture_width <=24: 
                #         stand_offs_quantity = 2 + 2
                    
                #     elif picture_width >=25 and picture_width <=36: 
                #         stand_offs_quantity = 3 + 3
                    
                #     elif picture_width >=37 and picture_width <=48: 
                #         stand_offs_quantity = 4 + 4
                    
                #     elif picture_width >=49 and picture_size_feet <=60: 
                #         stand_offs_quantity = 5 + 5 
                    
                #     else: 
                #         print (0)
                    
                    # print("hiiiii")
                    # stand_offs_price = ProductAttribute.objects.filter(variant_type_name_id=id).values('price')
                    # print("stand_offs_price per piece " + str(stand_offs_price))
                    # stand_offs_price = stand_offs_price[0]['price']
                    # stand_offs_price = stand_offs_price * stand_offs_quantity
                    # print(stand_offs_price)
                    
                    # total = melamine_base_price + melamine_front_price + melamine_back_price + stand_offs_price
                
                    # print("stand_offs_quantity "+ str(stand_offs_quantity))
                    # print("stand_offs_price "+ str(stand_offs_price))
                    # print("total " + str(total))

            return Response({'status':'status.HTTP_200_OK',"picture_height": 0,
            # "picture_width" : picture_width, "picture_size":picture_size, "picture_size_feet":picture_size_feet, "frame_width_size":frame_width_size,
            # "frame_height_size":frame_height_size, "frame_height_feet_size":frame_height_feet_size,
            # "frame_width_feet_size":frame_width_feet_size, "frame_feet_size":frame_feet_size,
            # "melamine_base_price": melamine_base_price, "melamine_front_price": melamine_front_price,
            # "melamine_back_price":melamine_back_price, "stand_offs_price": stand_offs_price, "total":total
            })
                    



   
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
#             frame_feet_size = 0
#             frame_height = 0
#             frame_height_feet = 0
#             for x in attributes:
#                 id = x['variant_type_id']
#                 value = x['value']

#                 name = Variant_type.objects.filter(id=id).values('variant_type_name', 'id')
#                 for x in name:
#                     type_name = x['variant_type_name']
#                     variant_type_id = x['id']

#                 if id == variant_type_id and type_name == 'picture height':
#                     picture_height = value
                
#                 if id == variant_type_id and type_name == 'picture width':
#                     picture_width = value
#                     picture_size = picture_height * picture_width
#                     picture_size_feet = picture_size / 12

#                     print("picture height "+ str(picture_height))
#                     print("picture_width "+ str(picture_width))
#                     print("picture_size "+ str(picture_size))
                 
#                 if id == variant_type_id and type_name == 'frame height':
#                     frame_height = value
                           
#                 if id == variant_type_id and type_name == 'frame width':
#                     frame_width = value
#                     frame_size = frame_height * frame_width

#                     frame_height_size = (picture_height+(2*frame_height))
#                     frame_height_feet_size = frame_height_size / 12

#                     frame_width_size = (picture_width+(2*frame_width)) 
#                     frame_width_feet_size = frame_width_size / 12
                     
#                     frame_feet_size = frame_height_feet_size * frame_width_feet_size
                    
#                     print("frame_height "+ str(frame_height))
#                     print("frame_height_feet "+ str(frame_height_feet))
#                     print("frame_width "+ str(frame_width))
#                     print("frame_size "+ str(frame_size))
#                     print("frame_feet_size "+ str(frame_feet_size))
                
#                     # melamine_name = Variant_type.objects.filter(id=id).values('variant_type_name', 'id')
#                     # melamine_base_price = ProductAttribute.objects.filter(variant_type_name_id=id).values('price')
#                     # print("melamine price is : " + str(melamine_name))
#                     melamine_base_price = Variant.objects.filter(variant_name='Melamine Base').values('price')
#                     melamine_base_price = melamine_base_price[0]['price']
#                     print(melamine_base_price)
#                     melamine_base_price = frame_feet_size*melamine_base_price

#                     melamine_front_price = Variant.objects.filter(variant_name='Melamine front').values('price')
#                     melamine_front_price = melamine_front_price[0]['price']
#                     print(melamine_front_price)
#                     melamine_front_price = frame_feet_size*melamine_front_price

#                     melamine_back_price = Variant.objects.filter(variant_name='Melamine back ').values('price')
#                     melamine_back_price = melamine_back_price[0]['price']
#                     print(melamine_back_price)
#                     melamine_back_price = frame_feet_size*melamine_back_price

#                     print("melamine_base_price "+ str(melamine_base_price))
#                     print("melamine_front_price "+ str(melamine_front_price))
#                     print("melamine_back_price "+ str(melamine_back_price))
                
#                     if picture_size_feet >=0 and picture_size_feet <=24: 
#                         stand_offs_quantity = 2 + 2
                    
#                     elif picture_size_feet >=25 and picture_size_feet <=36: 
#                         stand_offs_quantity = 3 + 3
                    
#                     elif picture_size_feet >=37 and picture_size_feet <=48: 
#                         stand_offs_quantity = 4 + 4
                    
#                     elif picture_size_feet >=49 and picture_size_feet <=60: 
#                         stand_offs_quantity = 5 + 5 
                    
#                     else: 
#                         print (0)
                    
#                     stand_offs_price = Variant.objects.filter(variant_name='stand offs').values('price')
#                     stand_offs_price = stand_offs_price[0]['price']
#                     stand_offs_price = stand_offs_price * stand_offs_quantity
#                     print(stand_offs_price)
                    
#                     total = melamine_base_price + melamine_front_price + melamine_back_price + stand_offs_price
                
#                     print("stand_offs_quantity "+ str(stand_offs_quantity))
#                     print("stand_offs_price "+ str(stand_offs_price))
#                     print("total " + str(total))

#             return Response({'status':'status.HTTP_200_OK',"picture_height": picture_height,
#             "picture_width" : picture_width, "picture_size":picture_size, "picture_size_feet":picture_size_feet, "frame_width_size":frame_width_size,
#             "frame_height_size":frame_height_size, "frame_height_feet_size":frame_height_feet_size,
#             "frame_width_feet_size":frame_width_feet_size, "frame_feet_size":frame_feet_size,
#             "melamine_base_price": melamine_base_price, "melamine_front_price": melamine_front_price,
#             "melamine_back_price":melamine_back_price, "stand_offs_price": stand_offs_price, "total":total})
                






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
