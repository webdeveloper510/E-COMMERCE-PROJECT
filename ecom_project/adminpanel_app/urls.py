from django.urls import path, include
from rest_framework.routers import DefaultRouter
from adminpanel_app import views

router = DefaultRouter()
router.register('logo', views.LogoViewSet,basename="Logo")
router.register('header', views.HeaderViewSet,basename="header")
router.register('banner', views.BannerViewSet,basename="banner")
router.register('services', views.ServicesViewSet,basename="services")
router.register('carousel', views.CarouselViewSet,basename="carousel")
router.register('testimonial', views.TestimonialViewSet,basename="testimonial")
router.register('heading-category', views.HeadingCategoryViewSet,basename="HeadingCategory")
router.register('headings', views.HeadingsViewSet,basename="headings")

urlpatterns = [
    path('', include(router.urls)),
]