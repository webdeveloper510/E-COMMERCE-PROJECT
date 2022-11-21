from django.contrib import admin
from django.urls import path,include
from payment_app import views
from rest_framework.routers import DefaultRouter
from payment_app.views import *
from django.conf import settings
#create router object
router = DefaultRouter()

#register class viewset
router.register('paypal', views.PaypalPaymentViewSet, basename='paypal') 
router.register('stripe', views.StripePaymentViewSet, basename="stripe")

urlpatterns = [
    path('', include(router.urls)),
    path('test/', views.test)
] 
