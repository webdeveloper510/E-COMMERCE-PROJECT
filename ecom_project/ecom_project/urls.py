from django.contrib import admin
from django.urls import path,include
from payment_app.views import *
from product_app import views, serializers
from rest_framework.routers import DefaultRouter

#create router object
router = DefaultRouter()

#register class viewset
router.register('category', views.CategoryViewSet, basename='category') 
router.register('product', views.ProductViewSet, basename='product') 
router.register('variant-type', views.Variant_typeViewSet,basename='variant_type')
router.register('variant', views.VariantViewSet,basename='variant')
router.register('product-attribute', views.ProductAttributeViewSet,basename='ProductAttribute')
#router.register('product-variant', views.ProductVariantViewSet,basename='ProductVariant')
#router.register('cart', views.CartViewSet ,basename='cart')
#router.register('delivery_cost', views.DeliveryCostViewSet,basename='delivery_cost')
#router.register('type', views.TypesViewSet,basename='types')
router.register('price', views.PriceViewSet, basename='price')
#router.register('product-order', views.Product_order, basename='product-order')
#router.register('total-price', views.Total_Price, basename='total-price')
router.register('totalprice', views.TotalpriceViewSet, basename='Totalprice')
router.register('order', views.OrderViewSet,basename='Order')
router.register('order-item', views.OrderItemViewSet,basename='Orderitem')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account_app.urls')),
    path('', include('payment_app.urls')),
    path('',include(router.urls)),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]