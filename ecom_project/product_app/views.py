<<<<<<< HEAD

from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets,status
from .helper import *
from rest_framework.decorators import action
from rest_framework.response import Response





class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('category_id')
    serializer_class = ProductSerializer

class Variant_typeViewSet(viewsets.ModelViewSet):
    queryset = Variant_type.objects.all().order_by('id')
    serializer_class = Variant_typeSerializer 

class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variant.objects.all().order_by('id')
    serializer_class = VariantSerializer 
    
class TypesViewSet(viewsets.ModelViewSet):
    queryset = Types.objects.all().order_by('id')
    sample_instance = Types.objects.get(id=4)
    value_of_name = sample_instance.price
    print(value_of_name)
    serializer_class = TypesSerializer 
    

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

class DeliveryCostViewSet(viewsets.ModelViewSet):
    queryset = DeliveryCost.objects.all().order_by('id')


=======

from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets,status
from .helper import *
from rest_framework.decorators import action
from rest_framework.response import Response



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

class DeliveryCostViewSet(viewsets.ModelViewSet):
    queryset = DeliveryCost.objects.all().order_by('id')
    serializer_class = DeliveryCostSerializer



    '''
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
'''
      
      



>>>>>>> 4f3611108582a09a769829a9512efd2cf461b586
