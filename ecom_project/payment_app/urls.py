from django.urls import path
from .views import *
from payment_app import views

urlpatterns = [
    path('', views.payment, name='payment'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('paypal/', views.paypal_home, name="paypal_home"),
    path('paypal-return', views.paypal_return, name="paypal-return"),
    path('paypal-cancel', views.paypal_cancel, name="paypal-cancel"),
    path('stripe/', HomePageView.as_view(), name='home'),
 ]