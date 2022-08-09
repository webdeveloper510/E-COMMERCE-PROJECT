from django.shortcuts import render
from .serializers import *


from rest_framework import viewsets,status
from .helper import *
from rest_framework.decorators import action
from rest_framework.response import Response



from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt 


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
