import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from product_app.models import Order, Shipping
from django.views.generic import TemplateView
import uuid
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import *
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from product_app.views import ShippingViewSet


#stripe
stripe.api_key = settings.API_SECRET_KEY

price = 0
class HomePageView(TemplateView):    
    template_name = 'home.html'
    def get_context_data(self, *args, **kwargs): 
            global price, total_price
            price = ShippingViewSet().ship(self.request)
            total_price = str(int(round(price, 2) * 100))
            context =super().get_context_data(**kwargs)        
            context['key'] = settings.API_PUBLISH_KEY   
            context['total_price'] = total_price
            return context

def charge(request):
      if request.method == 'POST':
        order_data = Order.objects.all()
        for x in order_data:
            order_id = x.id
            # print(order_id)
        charge = stripe.Charge.create(
            currency= 'usd',
            amount = total_price,
            description= 'Payment gateway',
            source= request.POST['stripeToken'],
            metadata= {'order_id': order_id},

        )
        # print(charge)
        s_amount = charge['amount'] 
        order = charge['order']
        customer_id = charge['id']
        name = charge['billing_details']['name']
        phone = charge['billing_details']['phone']
        country = charge['billing_details']['address']['country']
        city = charge['billing_details']['address']['city']
        postal_code = charge['billing_details']['address']['postal_code']
        state = charge['billing_details']['address']['state']
        payment_method = charge['payment_method']
        status = charge['status']
        charge_data = stripe_charge.objects.create(amount = s_amount,order= order,customer_id=customer_id,name=name,
                       phone=phone,country=country,city=city,postal_code=postal_code,
                       state=state,payment_method=payment_method,status=status)
        charge_data.save()
        return render(request, 'charge.html')



#paypal
class CheckoutView(View):
 def paypal_home(self, request):
    host = request.get_host()
    print('price is --', price)
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount':  '2',
        'item_name': 'Order {}'.format(order.id),
        'item_name': 'Product 1',
        'invoice': str(uuid.uuid4()),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return_url': f'http://{host}{reverse("paypal-return")}',
        'cancel_return': f'http://{host}{reverse("paypal-cancel")}',
         }
    form = PayPalPaymentsForm(initial=paypal_dict)
    print("paypal", form)
    paypal_context = {'form':form}
    return render(request, 'paypalhome.html', paypal_context )

def paypal_return(request):
    messages.success(request, 'You have successfully made a payment')
    return redirect('paypal_home')

def paypal_cancel(request):
    messages.success(request, 'Your order has been cancelled')
    return redirect('paypal_home')

# stripe.api_key = settings.API_SECRET_KEY

# class CreateCheckoutSessionView(View):

#     def post(self, request, *args, **kwargs):
#         price = Price.objects.get(id=self.kwargs["pk"])
#         print("price ---- ",price)
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     'price': price.stripe_price_id,
#                     'quantity': 1,
#                 },
#             ],
            
#             mode='payment',
#             success_url=settings.BASE_URL + '/success/',
#             cancel_url=settings.BASE_URL + '/cancel/',
#         )
#         return redirect(checkout_session.url)

# class SuccessView(TemplateView):
#     template_name = "success.html"

# class CancelView(TemplateView):
#     template_name = "cancel.html"  

# class HomePageView(TemplateView):
#     template_name = "home.html"

#     def get_context_data(self, **kwargs):
#         product = stripe_Product.objects.get(name="testing")
#         print(product)
#         prices = Price.objects.filter(product=product)
#         context = super(HomePageView, self).get_context_data(**kwargs)
#         context.update({
#             "product": product,
#             "prices": prices
#         })
#         return context

 
 #In views.py
# from django.conf import settings # new

# PaymentIntent stipe

from rest_framework.decorators import api_view, APIView, action
from rest_framework.response import Response
from rest_framework import status

class PaymentView(APIView):
    @action(detail=False, methods=['post','get'])
    def post(self, request, *args, **kwargs):
     try:
        amount = request.body
        paymentIntent = stripe.PaymentIntent.create(
            amount = 200,
            currency = "usd",
            payment_method_types=['card'],
            capture_method='manual',
            metadata={'integration_check': 'accept_a_payment'},
        ) 
        data = paymentIntent.client_secret

        return Response(data,status=status.HTTP_200_OK)
     except :
        return Response(status=status.HTTP_400_BAD_REQUEST)


# WEBHOOK STRIPE

# from django.views.decorators.csrf import csrf_exempt
# from django.http.response import JsonResponse, HttpResponse

# # This is your Stripe CLI webhook secret for testing your endpoint locally.
# endpoint_secret = 'whsec_y3qCLGvpYRxrmGeM7awuoCHG3DXccI2a'

# @csrf_exempt
# def stripe_webhook(request):
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return HttpResponse(status=400)

#     # Handle the checkout.session.completed event
#     if event['type'] == 'checkout.session.completed':
#         print("Payment was successful.")
#         # TODO: run some custom code here

#     return HttpResponse(status=200)

# @csrf_exempt
# def webhook_view(request):
#     payload = request.body
#     print ("payload" ,  payload)
#     return HttpResponse(status = 200)



# 21.09.2022
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        print("Data received from Webhook is: ", request.body)
        return HttpResponse("Webhook received!")

# class call(object):
#     def __init__(self, path='/home/gurpreet/Desktop/GK/E-COMMERCE-PROJECT/ecom_project/product_app/views.py'):
#         self.path= path

#     def callfile(self):
#         call(['python3','{}'.format(self.path)])

# if __name__ == "__main__":
#     c = call()
#     c.callfile()




# https://raturi.in/blog/django-stripe-integration-fully-explained-example/      
