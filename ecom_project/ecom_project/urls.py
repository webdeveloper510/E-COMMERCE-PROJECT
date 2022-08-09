from django.contrib import admin
from django.urls import path,include
from payment_app.views import *
from product_app import views
from rest_framework.routers import DefaultRouter
#create router object
router = DefaultRouter()

#register class viewset
router.register('category', views.CategoryViewSet, basename='category') 
router.register('product', views.ProductViewSet, basename='product')
router.register('cart', views.CartViewSet ,basename='cart')
router.register('delivery_cost', views.DeliveryCostViewSet,basename='delivery_cost')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account_app.urls')),
    path('', include('payment_app.urls')),
    path('',include(router.urls)),
    path('paypal/', include('paypal.standard.ipn.urls')),
]