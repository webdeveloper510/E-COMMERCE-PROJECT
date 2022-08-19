from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product_app.helper import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Sum


class Variant_typeViewSet(viewsets.ModelViewSet):
    queryset = Variant_type.objects.all().order_by('id')
    serializer_class = Variant_typeSerializer

class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variant.objects.all().order_by('id')
    serializer_class = VariantSerializer

class ProductAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductAttribute.objects.all().order_by('id')
    sample_instance = ProductAttribute.objects.get(id=4)
    value_of_name = sample_instance.price
    #print(value_of_name)
    serializer_class = ProductAttributeSerializer

class  ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all().order_by('id')
    serializer_class = ProductVariantSerializer

class TypesViewSet(viewsets.ModelViewSet):
    queryset = Types.objects.all().order_by('id')
    serializer_class = TypesSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('category_id')
    serializer_class = ProductSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all().order_by('id')
    serializer_class = CartSerializer
    @action(methods=['get'], detail=False, url_path='checkout/(?P<userId>[^/.]+)', url_name='checkout')
    def checkout(self, request, *args, **kwargs):

        try:
            user = User.objects.get(pk=int(kwargs.get('userId')))
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'Error': str(e)})

        cart_helper = CartHelper(user)
        checkout_details = cart_helper.prepare_cart_for_checkout()

        if not checkout_details:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'error': 'Cart of user is empty.'})

        return Response(status=status.HTTP_200_OK, data={'checkout_details': checkout_details})

class DeliveryCostViewSet(viewsets.ViewSet):
    queryset = DeliveryCost.objects.all().order_by('id')
    serializer_class = DeliveryCostSerializer


class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all().order_by('id')
    serializer_class = PriceSerializer


class TotalPriceViewSet(viewsets.ModelViewSet):
    queryset = Total_Price.objects.all().order_by('id')
    serializer_class = Total_PriceSerializer
    total_variant_price = Price.objects.all().aggregate(total_variant_price=Sum('variant_price'))['total_variant_price']
    print(total_variant_price)
    
'''
class PriceViewSet(viewsets.ModelViewSet):  
    queryset = Price.objects.all().order_by('id')
    p_queryset = ProductAttribute.objects.all().order_by('id')
    price_instance = Price.objects.get(id=1)
    product_instance = ProductAttribute.objects.get(id=1)
    type = price_instance.type_id
    value = price_instance.value
    price = product_instance.price
    total_price = price * value
    #total_price = total_price + total_price
    print(total_price)
    #print(price)
    serializer_class = PriceSerializer

    http_method_names = ['get']
    def retrieve(self, request, pk=None):
        instance = self.get_object()
        # query = request.GET.get('query', None)  # read extra data
        return Response(self.serializer_class(instance).data,
                        status=status.HTTP_200_OK)



    



def total_price(self):
        total = self.total_price + self.total_price 
        return total
    #Price.objects.annotate(total=F('type_id') * F('price'))  



    @action(detail=True, methods=['get'])
    def get_price(self, request, pk=type):
        id=type
        if id is not None:
            price_instance = Price.objects.get(id=id)
            price = price_instance.price
            serializer_class = PriceSerializer
            print(price)
            return Response({'msg':'Data Created'})

    
   def retrieve(self, queryset, request, pk=None):
        type = pk
        id=type
        if id is not None:
            price_instance = Price.objects.get(id=id)
            price = price_instance.price
            serializer_class = PriceSerializer
            print(price)
            return Response({'msg':'Data Created'})

    def cart(request):
            total = Cart.objects.annotate(
                price=Sum(F('orderitem__item__price') * F('orderitem__quantity'))
            ).get(
                order_user=request.user
            )
            cart.total = cart.price
            cart.save()
   
   


class CategoryViewSet(viewsets.ViewSet):
    #http_method_names = ['get', 'post']
    @csrf_exempt   
    def list(self, request):
        Category_data = Category.objects.all()
        serializer = CategorySerializer(Category_data, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'})
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            Category_data = Category.objects.get(id=id)
            serializer = CategorySerializer(Category_data)
            return Response(serializer.data)

    def update(self, request, pk):
        id = pk
        Category_data = Category.objects.get(pk=id)
        serializer = CategorySerializer(Category_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data updated'})
        return Response(serializer.errors)
    
    def partial_update(self, request, pk):
        id = pk
        Category_data = Category.objects.get(pk=id)
        serializer = CategorySerializer(Category_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partially data updated'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        Category_data = Category.objects.get(pk=id)
        Category_data.delete()
        return Response({'msg':'Data Deleted'})



class ProductViewSet(viewsets.ViewSet):
    #http_method_names = ['get', 'post']
    @csrf_exempt   

    def list(self, request):
        Product_data = Product.objects.all()
        serializer = ProductSerializer(Product_data, many=True)
        return Response(serializer.data)
  
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'})
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            Product_data = Product.objects.get(id=id)
            serializer = ProductSerializer(Product_data)
            return Response(serializer.data)

    def update(self, request, pk):
        id = pk
        Product_data = Product.objects.get(pk=id)
        serializer = ProductSerializer(Product_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data updated'})
        return Response(serializer.errors)
    
    def partial_update(self, request, pk):
        id = pk
        Product_data = Product.objects.get(pk=id)
        serializer = ProductSerializer(Product_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partially data updated'})
        return Response(serializer.errors)

    def destroy(self, request, pk):
        id = pk
        Product_data = Product.objects.get(pk=id)
        Product_data.delete()
        return Response({'msg':'Data Deleted'})


    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        print(params['pk'])
        Product_data = Product.objects.filter(name=params['pk'])
        serializer = ProductSerializer(Product_data, many=True)
        return Response(serializer.data)

      
  
class PriceViewSet(viewsets.ViewSet):
    @api_view(['GET', 'POST'])
    def hello_world(request):
        if request.method == 'POST':
            return Response({"message": "Got some data!", "data": request.data})
        return Response({"message": "Hello, world!"})
'''


class Product_order(viewsets.ViewSet):
    #http_method_names = ['get', 'post']
    @csrf_exempt   

    def list(self, request):
        Price_data = Price.objects.all()
        serializer = PriceSerializer(Price_data, many=True)
        return Response(serializer.data)
  
    def create(self, request):
        serializer = PriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'})
        return Response(serializer.errors)


    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            price_instance = Price.objects.get(id=id)
            product_instance = ProductAttribute.objects.get(id=id)
            type = price_instance.type_id
            value = price_instance.value
            price = product_instance.price
            variant_price = price * value
            return Response({'type_id':type, 'value':value, 'price':price, 'variant_price':variant_price })
            
    def destroy(self, request, pk):
        id = pk
        Product_data = Price.objects.get(pk=id)
        Product_data.delete()
        return Response({'msg':'Data Deleted'})

    
    

class Total_Price(viewsets.ViewSet):
    @csrf_exempt   

    def list(self, request):
        Total_Price_data = Total_Price.objects.all()
        serializer = Total_PriceSerializer(Total_Price_data, many=True)
        return Response(serializer.data)
  
    def create(self, request):
        serializer = Total_PriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'})
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            Total_Price_data = Total_Price.objects.get(id=id)
            serializer = Total_PriceSerializer(Total_Price_data)
            return Response(serializer.data)

           
    #Price.objects.annotate(total=F('type_id') * F('price'))  
