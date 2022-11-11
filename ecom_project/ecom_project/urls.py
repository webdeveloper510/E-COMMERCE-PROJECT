from django.contrib import admin
from django.urls import path,include
from product_app import views, serializers
from rest_framework.routers import DefaultRouter
from product_app.views import *
from django.conf import settings
from django.conf.urls.static import static
#create router object
router = DefaultRouter()

#register class viewset
router.register('category', views.CategoryViewSet, basename='category') 
router.register('product', views.ProductViewSet, basename='product') 
router.register('elements', views.ElementsViewSet,basename='elements')
router.register('variant', views.VariantViewSet,basename='variant')
router.register('variant-type', views.Variant_typeViewSet,basename='variant_type')
router.register('product-attribute', views.ProductAttributeViewSet,basename='ProductAttribute')
router.register('calculateprice', views.CalculatePriceViewSet, basename='calculatePrice')
router.register('list', views.Send_listViewSet, basename = 'Send_listViewSet')
router.register('product_list', views.product_listViewSet, basename = 'product_listViewSet')
router.register('order', views.OrderViewSet, basename = 'list_OrderViewSet')
router.register('shipping', views.ShippingViewSet, basename = 'ShippingViewSet')
router.register('dashboard', views.DashboardViewSet, basename = 'DashboardViewSet')
router.register('image', views.Frame_ImageViewSet, basename = 'Frame_ImageViewSet')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account_app.urls')),
    path('', include('payment_app.urls')),
    path('', include('adminpanel_app.urls')),
    path('',include(router.urls)),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('auth/', include('rest_framework.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "UMSRA Admin"
admin.site.site_title = "UMSRA Admin Portal"
admin.site.index_title = "Welcome to Frame-Art "