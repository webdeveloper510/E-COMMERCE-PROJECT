from django.urls import path, include
from rest_framework.routers import DefaultRouter
from adminpanel_app import views
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register('logo', views.LogoViewSet,basename="Logo")
router.register('url', views.URLViewSet,basename="url")
router.register('header', views.HeaderViewSet,basename="header")
router.register('banner', views.BannerViewSet,basename="banner")
router.register('services', views.ServicesViewSet,basename="services")
router.register('FAQ', views.FAQViewSet,basename="FAQ")
router.register('logolist', views.logolistViewSet,basename="logolist")
router.register('headerlist', views.headerlistViewSet,basename="headerlist")
router.register('bannerlist', views.bannnerlistViewSet,basename="bannerlist")
router.register('serviceslist', views.serviceslistViewSet,basename="serviceslist")
router.register('FAQlist', views.FAQlistViewSet,basename="FAQlist")

urlpatterns = [
    path('adminpanel/', include(router.urls)),
] 