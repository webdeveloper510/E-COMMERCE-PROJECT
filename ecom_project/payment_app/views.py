from unicodedata import name
import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from .models import Price,Product
from django.views.generic import TemplateView

import uuid
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import *
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings


def payment(request):
    return render(request, 'payments.html')

#paypal
def paypal_home(request):
   # host = request.get_host()
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '1',
        'item_name': 'Order {}'.format(order.id),
        'item_name': 'Product 1',
        'invoice': str(uuid.uuid4()),
        #'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return_url': f'http://{host}{reverse("paypal-return")}',
        'cancel_return': f'http://{host}{reverse("paypal-cancel")}',
         }
    form = PayPalPaymentsForm(initial=paypal_dict)
    paypal_context = {'form':form}
    return render(request, 'paypalhome.html', paypal_context )

def paypal_return(request):
    messages.success(request, 'You have successfully made a payment')
    return redirect('paypal_home')

def paypal_cancel(request):
    messages.success(request, 'Your order has been cancelled')
    return redirect('paypal_home')


#stripe
stripe.api_key = settings.API_SECRET_KEY

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        price = Price.objects.get(id=self.kwargs["pk"])
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=settings.BASE_URL + '/success/',
            cancel_url=settings.BASE_URL + '/cancel/',
        )
        return redirect(checkout_session.url)

class SuccessView(TemplateView):
    template_name = "success.html"

class CancelView(TemplateView):
    template_name = "cancel.html"  

class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Test Product")
        print(product)
        prices = Price.objects.filter(product=product)
        context = super(HomePageView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "prices": prices
        })
        return context      
      
