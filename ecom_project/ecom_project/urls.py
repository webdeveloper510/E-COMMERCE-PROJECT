from django.contrib import admin
from django.urls import path,include
from payment_app.views import *
from product_app import views
from rest_framework.routers import DefaultRouter
from product_app.views import *
#create router object
router = DefaultRouter()

#register class viewset
router.register('category', views.CategoryViewSet, basename='category') 
router.register('product', views.ProductViewSet, basename='product') 
router.register('elements', views.ElementsViewSet,basename='elements')
router.register('variant', views.VariantViewSet,basename='variant')
router.register('variant-type', views.Variant_typeViewSet,basename='variant_type')
router.register('width', views.WidthViewSet,basename='width')
router.register('product-attribute', views.ProductAttributeViewSet,basename='ProductAttribute')#router.register('calculateprice', views.CalculatePriceViewSet,basename='calculatePrice')
router.register('calculateprice', views.CalculatePriceViewSet, basename='calculatePrice')
router.register('list', views.Variant_type_list_ViewSet, basename='list_of_array')
router.register('type', views.TypeViewSet, basename = 'Type')
router.register('dict', views.Send_listViewSet, basename = 'list')



#router.register('variant-type', views.Variant_typeViewSet,basename='variant_type')
#router.register('variant', views.VariantViewSet,basename='variant')
#router.register('type', views.TypesViewSet,basename='types')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account_app.urls')),
    path('', include('payment_app.urls')),
    path('',include(router.urls)),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]