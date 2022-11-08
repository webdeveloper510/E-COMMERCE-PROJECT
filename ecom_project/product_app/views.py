from .serializers import *
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from product_app.models import *

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

class product_listViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]
    @csrf_exempt 
    @action(detail=False, methods=['post','get'])
    def post(self, request, *args, **kwargs):
      if request.method == 'POST':
        queryset = Product.objects.all().values('id','name','description','category__id','category__name') 
        array = []
        for x in queryset:
            category_id = x['category__id']
            category_name= x['category__name']
            product_id = x['id']
            product_name = x['name']
            queryset = {'category_id':x['category__id'],'category_name':x['category__name'],'product_id':x['id'],'product_name':x['name']}
            array.append(queryset)
      return Response(array)

class Send_listViewSet(viewsets.ViewSet):
    @csrf_exempt 
    @action(detail=False, methods=['post','get'])
    def post(self, request, *args, **kwargs):
      if request.method == 'POST':
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
      return Response(array)

total = 0
class CalculatePriceViewSet(viewsets.ViewSet):
    @csrf_exempt 
    @action(detail=False, methods=['POST'])
    def price(self, request, format=None):
        global total
        if request.method == 'POST':
            user_id = request.data.get('user_id')
            attributes = request.data.get('attributes')
            category_id = request.data.get('category_id')
            product_id = request.data.get('product_id')
            quantity = request.data.get('quantity')
            for x in attributes:
                id = x['variant_type_id']
                value = x['value']
                name = Variant_type.objects.filter(id=id).values('variant_type_name', 'variant_id','id','variant','variant__variant_name','variant__element','variant__element__element')
                
                if id == name[0]['id'] and name[0]['variant__element__element']  == 'Frame length':
                    frame_length = value

                elif id == name[0]['id'] and name[0]['variant__element__element']  == 'Frame width':
                    frame_width = value

                elif id == name[0]['id'] and name[0]['variant__element__element'] == 'Picture length':
                    picture_length = value
                           
                elif id == name[0]['id'] and name[0]['variant__element__element']  == 'Picture width':
                    picture_width = value

                    frame_feet_length = picture_length + (2 * frame_length)
                    frame_feet_length = frame_feet_length / 12

                    frame_feet_width =  picture_width + (2 * frame_width)
                    frame_feet_width = frame_feet_width / 12
                    frame_feet_size = frame_feet_length * frame_feet_width

                elif id == name[0]['id'] and name[0]['variant__element__element']  == 'Base color':
                    b__price = ProductAttribute.objects.filter(variant_type_name_id=name[0]['id'],category_id=category_id,product_id=product_id).values('price')
                    base_price = frame_feet_size * b__price[0]['price']

                elif id == name[0]['id'] and name[0]['variant__element__element']  == 'Front color':
                    f_price = ProductAttribute.objects.filter(variant_type_name_id=name[0]['id'],category_id=category_id,product_id=product_id).values('price')
                    front_price = frame_feet_size * f_price[0]['price']
                
                elif id == name[0]['id'] and name[0]['variant__element__element']  == 'Back color':
                    bck_price = ProductAttribute.objects.filter(variant_type_name_id=name[0]['id'],category_id=category_id,product_id=product_id).values('price')
                    back_price = frame_feet_size * bck_price[0]['price']
                
                    if picture_width >=0 and picture_width <=24: 
                        stand_offs_quantity = 2 + 2
                    
                    if picture_width >=25 and picture_width <=36: 
                        stand_offs_quantity = 3 + 3
                    
                    if picture_width >=37 and picture_width <=48: 
                        stand_offs_quantity = 4 + 4
                    
                    if picture_width >=49 and picture_width <=60: 
                        stand_offs_quantity = 5 + 5 
                
                elif id == name[0]['id'] and name[0]['variant__element__element']  == 'Stand off':
                    s_price = ProductAttribute.objects.filter(variant_type_name_id=name[0]['id'],category_id=category_id,product_id=product_id).values('price','unit')
                    stand_offs_price = s_price[0]['price'] * s_price[0]['unit']
                    stand_offs_price = stand_offs_quantity * stand_offs_price
            total = base_price + front_price + back_price + stand_offs_price
            total = total * quantity

            return Response({"frame_length":frame_length,"frame_width":frame_width,
            "picture_length":picture_length,"picture_width":picture_width,"frame_feet_length":frame_feet_length,
            "frame_feet_width":frame_feet_width,"frame_feet_size":frame_feet_size,
            "base_price":(b__price[0]['price'],base_price),"front_price":(f_price[0]['price'],front_price),
            "back_price":(bck_price[0]['price'],back_price),"stand_offs_quantity":stand_offs_quantity,
            "stand_offs_price":(s_price[0]['price'],stand_offs_price),"Total":total, 
            })
        return total
    

class OrderViewSet(viewsets.ViewSet):
    @csrf_exempt 
    @action(detail=False, methods=['post'])
    def post(self, request, format=None):
        global order_id, product_name
        if request.method == 'POST':
            # image= request.FILES['image']
            user_id = request.data.get('user_id')
            item = request.data.get('items')
            status = request.data.get('status')
            email = request.data.get('email')
            contact = request.data.get('contact')
            name = request.data.get('name')
            street_address = request.data.get('street_address')
            apartment = request.data.get('apartment')
            city = request.data.get('city')
            state = request.data.get('state')
            zip_code = request.data.get('zip_code')
            total = request.data.get('total')
            for i in item:
                price = i['price']
                quantity = i['quantity']
                value = i['value']
                product_name = i['product_name']
            order_data = Order.objects.create(item = i['value'], product = product_name, status = status, user_id = user_id,
                                                 email = email, contact=contact, quantity = quantity, 
                                                 name=name, street_address = street_address, 
                                                 apartment=apartment, city =city, state=state, 
                                                 zip_code=zip_code,total=total)
            serializer = OrderSerializer(data=order_data)
            order_data.save()  
            order_id = Order.objects.filter(user_id = user_id).values('id')
            order_id = order_id[0]['id']
            return JsonResponse({"user_id": user_id, "order_id": order_id, "item":item, "status":status, "user_id":user_id, "email":email, "contact":contact,
                                 "quantity":1, "name":name, "street_address":street_address,
                                     "apartment":apartment, "city":city, "state":state,"zip_code":zip_code})
        
    

class ShippingViewSet(viewsets.ViewSet):
    @csrf_exempt 
    @action(detail=False, methods=['post'])
    def post (self, request, *args, **kwargs):
        global total_price
        user_id = 0
        order_id = 0
        if request.method == 'POST':
            percentage = Shipping.objects.all().values('percentage')
            total_price =  total + percentage[0]['percentage']
            return Response(total_price)
        return total_price


class DashboardViewSet(viewsets.ViewSet):
    @csrf_exempt 
    @action(detail=False, methods=['post'])
    def users(self, request, *args, **kwargs):
            users = User.objects.all().filter(is_admin=0).count()
            print(users)
            return Response(users)
    
    @csrf_exempt 
    @action(detail=False, methods=['post'])
    def email(self, request, *args, **kwargs):
            email = User.objects.all().filter(is_admin=0).values('email')
            print(email)
            return Response(email)

#Total orders
    @csrf_exempt
    @action(detail=False, methods=['post'])
    def order(self, request, *args, **kwargs):
        total_orders = Order.objects.all().values('item').count()
        print('order items', total_orders)
        return Response(total_orders)

    @csrf_exempt 
    @action(detail=False, methods=['post'])
    def pending(self, request, *args, **kwargs):
            pending_order = Order.objects.all().filter(status = 'pending').values('item').count()
            print(pending_order)
            return Response(pending_order)

    @csrf_exempt 
    @action(detail=False, methods=['post'])
    def success(self, request, *args, **kwargs):
            pending_order = Order.objects.all().filter(status = 'success').values('item').count()
            print(pending_order)
            return Response(pending_order)

    @csrf_exempt 
    @action(detail=False, methods=['post'])
    def failed(self, request, *args, **kwargs):
            pending_order = Order.objects.all().filter(status = 'failed').values('item').count()
            print(pending_order)
            return Response(pending_order)

    # https://github.com/OkothPius/Masoko-Ecommerce/blob/main/ecommerce/models.py