from django.urls import path
from payment_app.views import *
from payment_app import views
from product_app.views import *

# urlpatterns = [
#     path('cancel/', CancelView.as_view(), name='cancel'),
#     path('success/', SuccessView.as_view(), name='success'),
#     path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
   
    
#  ]

urlpatterns = [
    path('stripe/', HomePageView.as_view(), name='home'),
    path('charge/', views.charge, name='charge'),
    # path('webhook/', views.stripe_webhook), 
    path('paymentintent/', PaymentView.as_view(), name='payment'),
    path('paypal/', CheckoutView.as_view(), name="paypal_home"),
    path('paypal-return', views.paypal_return, name="paypal-return"),
    path('paypal-cancel', views.paypal_cancel, name="paypal-cancel"),
    path('stripe/', HomePageView.as_view(), name='home'),
     
 ]