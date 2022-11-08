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
    path('stripe/', views.card_token),
    path('paypal/', views.get_paypal_access_token),
    path('paypal/capturepayment/', views.capture_payment),
    path('test/', views.test),
    path('spdf/', views.s_pdf),
    path('mail/',views.mail),
    path('receipt/', views.generate_pdf),
    # path('test/', views.test),
    # path('test/', views.test),
    # path('test/', views.test),
    # path('test/', views.test),
    # path('create-checkout-session/', StripeCheckoutView.as_view()),
    # path('pay/', StripeView.as_view()),
    # path('paypalorder/', views.create_order),
    # path('paypalorder/', views.payment_create),

    


 ]