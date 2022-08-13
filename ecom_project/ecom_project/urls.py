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
router.register('variant_type', views.Variant_typeViewSet,basename='variant_type')
router.register('variant', views.VariantViewSet,basename='variant')
router.register('types', views.TypesViewSet,basename='types')
router.register('ProductVariant', views.ProductVariantViewSet,basename='types')
router.register('ProductAttribute', views.ProductAttributeViewSet,basename='ProductAttribute')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account_app.urls')),
    path('', include('payment_app.urls')),
    path('',include(router.urls)),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]