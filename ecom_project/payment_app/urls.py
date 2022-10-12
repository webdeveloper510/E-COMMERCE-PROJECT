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
    path('customer/', views.home),
    path('cardid/', views.card),
    path('payment/', views.payment_intent),
    path('token/', views.card_token),
    path('charge/', views.charge),
    path('paypaltoken/', views.tok),
    path('paypalorder/', views.create_order),
    path('capture/', views.capture_payment),
    # path('cbc/', views.cbc),
    # path('cbc/', views.cbc),
    # path('cbc/', views.cbc),
    # path('cbc/', views.cbc),
    # path('cbc/', views.cbc),


    # path('create-checkout-session/', StripeCheckoutView.as_view()),
    # path('pay/', StripeView.as_view()),
    # path('token/', views.token),
    # path('paypalorder/', views.create_order),
    # path('paypalorder/', views.payment_create),

    
    




    # path('stripe/', HomePageView.as_view(), name='home'),
    # path('charge/', views.charge, name='charge'),
    # # path('test-payment/$', views.test_payment),
    # # path('webhook/', views.stripe_webhook), 
    # path('paymentintent/', PaymentView.as_view(), name='payment'),
    # path('paypal/', views.paypal_home, name="paypal_home"),
    # path('paypal-return', views.paypal_return, name="paypal-return"),
    # path('paypal-cancel', views.paypal_cancel, name="paypal-cancel"),
    # path('stripe/', HomePageView.as_view(), name='home'),
    # path('test/', views.create_checkout_session, name='test'),
    # path('paypaltest/', views.paypal_head, name= "PaypalToken"),
    

 ]