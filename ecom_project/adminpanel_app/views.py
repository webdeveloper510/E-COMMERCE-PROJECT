from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *

class LogoViewSet(viewsets.ModelViewSet):
    queryset = Logo.objects.all()
    serializer_class = LogoSerializer

class HeaderViewSet(viewsets.ModelViewSet):
    queryset = Header.objects.all()
    serializer_class = HeaderSerializer

class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    
class ServicesViewSet(viewsets.ModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer

class CarouselViewSet(viewsets.ModelViewSet):
    queryset = Carousel.objects.all().order_by('id')
    serializer_class = CarouselSerializer
    
class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all().order_by('id')
    serializer_class = TestimonialSerializer

class HeadingCategoryViewSet(viewsets.ModelViewSet):
    queryset = HeadingCategory.objects.all().order_by('id')
    serializer_class = HeadingcategorySerializer

class HeadingsViewSet(viewsets.ModelViewSet):
    queryset = Headings.objects.all().order_by('id')
    serializer_class = HeadingsSerializer
