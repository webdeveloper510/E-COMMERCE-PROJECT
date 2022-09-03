from .serializers import *
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('category_id')
    serializer_class = ProductSerializer

class ElementsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Elements.objects.all().order_by('id')
    serializer_class = ElementsSerializer
    
class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variant.objects.all().order_by('id')
    serializer_class = VariantSerializer

class Variant_typeViewSet(viewsets.ModelViewSet):
    queryset = Variant_type.objects.all().order_by('id')
    serializer_class = Variant_typeSerializer
    
class ProductAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductAttribute.objects.all().order_by('id')
    serializer_class = ProductAttributeSerializer
          
class Send_listViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        queryset = Variant.objects.all().values('variant_name','field_type')
        types = Variant_type.objects.all().values('variant_type_name')
        dropdown = Variant.objects.all().values('id','variant_name','field_type','element__id') 
        array = []
        for x in dropdown:
            variant_id = x['id']
            variant_name= x['variant_name']
            field_Type = x['field_type']
            element_id = x['element__id']
            dropdown_options = Variant_type.objects.filter(variant=variant_id).values('id','variant_type_name')
            queryset = {'Field_type':field_Type,'Title':variant_name,'variant_id':variant_id,'element_id':element_id,'options':dropdown_options}
            array.append(queryset)
        return Response({'list':array})


class CalculatePriceViewSet(viewsets.ViewSet):
    @csrf_exempt 
    @action(detail=False, methods=['post','get'])
    def price(self, request, *args, **kwargs):
        if request.method == 'POST':
            attributes = request.data.get('attributes')
            category_id = request.data.get('category_id')
            product_id = request.data.get('product_id')
            frame_feet_size, frame_length, frame_width, picture_length, picture_width = 0,0,0,0,0
            base_price, back_price, front_price, stand_offs_quantity, stand_offs_price, total = 0,0,0,0,0,0
            for x in attributes:
                id = x['variant_type_id']
                value = x['value']
                name = Variant_type.objects.filter(id=id).values('variant_type_name', 'variant_id','id','variant','variant__variant_name','variant__element','variant__element__element')
                if id == name[0]['id'] and name[0]['variant__element__element']  == 'Picture length':
                    picture_length = value

                if id == name[0]['id'] and name[0]['variant__element__element']  == 'Picture width':
                    picture_width = value

                if id == name[0]['id'] and name[0]['variant__element__element'] == 'Frame length':
                    frame_length = value
                           
                if id == name[0]['id'] and name[0]['variant__element__element']  == 'Frame width':
                    frame_width = value
                    frame_feet_length = picture_length + (2 * frame_length)
                    frame_feet_length = frame_feet_length / 12
                    frame_feet_width =  picture_width + (2 * frame_width)
                    frame_feet_width = frame_feet_width / 12
                    frame_feet_size = frame_feet_length * frame_feet_width
                  
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
   
            return Response({'status':'status.HTTP_200_OK',"picture_length": picture_length,
             "picture_width":picture_width,"frame_length":frame_length,"frame_width":frame_width,
             "frame_feet_length":frame_feet_length,"frame_feet_width":frame_feet_width,
             "frame_feet_size":frame_feet_size, "base_price":(b__price[0]['price'],base_price),
             "front_price":(f_price[0]['price'],front_price),"back_price":(bck_price[0]['price'],back_price),
             "stand_offs_quantity":stand_offs_quantity,"stand_offs_price":(s_price[0]['price'],stand_offs_price),
             "total":total,
            })
