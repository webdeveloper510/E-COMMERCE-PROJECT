from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import viewsets

class LogoViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = LogoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            first = Logo.objects.first()
            queryset = Logo.objects.filter(id=first.id).update(image=serializer.data['image'])
            if Logo.objects.all().count() > 1:
                Logo_data = Logo.objects.get(id=serializer.data['id'])
                Logo_data.delete()
            return Response(serializer.data)
        return Response(serializer.errors)

class HeaderViewSet(viewsets.ModelViewSet):
    queryset = Header.objects.all().order_by('id')
    serializer_class = HeaderSerializer

class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all().order_by('id')
    serializer_class = BannerSerializer
    
class ServicesViewSet(viewsets.ModelViewSet):
    queryset = Services.objects.all().order_by('id')
    serializer_class = ServicesSerializer

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all().order_by('id')
    serializer_class = FAQSerializer
 
class logolistViewSet(viewsets.ViewSet):
    def list(self, request):
        image = Logo.objects.all().values('image')
        return Response(image)

class headerlistViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Header.objects.all()
        serializer = HeaderSerializer(queryset, many=True)
        return Response(serializer.data)

class bannnerlistViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Banner.objects.all()
        serializer = BannerSerializer(queryset, many=True)
        return Response(serializer.data)

class serviceslistViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Services.objects.all()
        serializer = ServicesSerializer(queryset, many=True)
        return Response(serializer.data)

class FAQlistViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = FAQ.objects.all()
        serializer = FAQSerializer(queryset, many=True)
        return Response(serializer.data)

