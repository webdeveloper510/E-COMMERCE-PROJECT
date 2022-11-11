from http.client import HTTPResponse
from queue import Empty
import stripe
from django.conf import settings
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from payment_app.models import *
from product_app.views import *
from product_app.models import *
from base64 import b64encode
import base64
import requests
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import json
from django.views.decorators.csrf import csrf_exempt
from account_app.utils import Util
from product_app.serializers import *
from product_app.models import *
from django.core.mail import send_mail
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.core.mail import EmailMultiAlternatives, message
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str,force_bytes, DjangoUnicodeDecodeError

#stripe
stripe.api_key = settings.API_SECRET_KEY

#create card token to use it in charge and name to create customer id
@csrf_exempt
@api_view(['POST'])
def card_token(request):
            global card_id, card_token, name , receipt_url
            user_id = request.data.get('user_id')
            order_id = request.data.get('order_id')
            total = request.data.get('total')
            name = request.data.get('name')
            email = request.data.get('email')
            number = request.data.get('number')
            exp_month = request.data.get('exp_month')
            exp_year = request.data.get('exp_year')
            cvc = request.data.get('cvc')
            price = str(int(round(total, 2) * 100))
            try:
                token_data = stripe.Token.create(
                card={
                    "name" : name,
                    "number": number,
                    "exp_month": exp_month,
                    "exp_year": exp_year,
                    "cvc": cvc,
                }, )
                card_token = token_data['id']
                card_id = token_data['card']['id']
                pass
            except stripe.error.CardError as error:
                print("pm erros is --", error.user_message)
                print("error is --", stripe.error.CardError, error)
                return Response(error.user_message)

            if card_token == card_token:
                customer_data = stripe.Customer.create( name = name, email = email)
                customer_id = customer_data['id']

            if customer_id == customer_id:
                source_data = stripe.Customer.create_source(customer_id,source = card_token)

            if source_data == source_data:
                payment_intent = stripe.PaymentIntent.create(
                customer = customer_id,
                amount= price,
                currency="usd",
                payment_method_types=["card"],
                payment_method = card_id,
                confirmation_method = 'automatic',
                confirm=True,
                receipt_email= email, 
                metadata= {'order_id': order_id, 'name': name, 'user_id': user_id},
                )
                payment_intent_id = payment_intent['id']
                status = payment_intent['status']
                
                receipt_url = payment_intent['charges']['data'][0]['receipt_url']
                charge_data = stripe_payment.objects.create( 
                name =  payment_intent['charges']['data'][0]['metadata']['name'], 
                user_id = payment_intent['charges']['data'][0]['metadata']['user_id'], 
                order_id = payment_intent['charges']['data'][0]['metadata']['order_id'],
                email =  payment_intent['charges']['data'][0]['receipt_email'],
                amount_received=  payment_intent['charges']['data'][0]['amount_captured'],
                payment_intent_id= payment_intent['id'], 
                charge_id= payment_intent['charges']['data'][0]['id'],
                amount_refund = payment_intent['charges']['data'][0]['amount_refunded'],
                billing_details = payment_intent['charges']['data'][0]['billing_details']['address'],
                currency = payment_intent['charges']['data'][0]['currency'],
                payment_method =  payment_intent['charges']['data'][0]['payment_method_details']['card'],
                created_id = payment_intent['charges']['data'][0]['created'],
                )
                receipt_url = urlsafe_base64_encode(force_bytes(receipt_url))
                charge_data.save()
                if status == "succeeded":
                    body = receipt_url
                    data = {
                        'subject':'Stripe Payment Receipt',
                        'body':body,
                        'to_email': email
                    }
                    Util.send_email(data)
                    order_data = Order.objects.filter(user_id=user_id).update(status='completed')
            return Response(card_id)      


def s_pdf(request):
    payment = capture_payment(request)
    template_path = receipt_url
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Receipt.pdf"'
    html = render_to_string(template_path, {'report': 123})
    pisaStatus = pisa.CreatePDF(html, dest=response)
    return response

#paypal
@csrf_exempt
@api_view(['POST'])
def get_paypal_access_token(request):
    global total, email, user_id, order_id, paypal_access_token, aprroval_link, capture_url, paypal_order_id, user_id, order_id
    user_id = request.data.get('user_id')
    order_id = request.data.get('order_id')
    total = request.data.get('total')
    name = request.data.get('name')
    email = request.data.get('email')

    encoded_auth = base64.b64encode((settings.CLIENT_ID + ':' + settings.CLIENT_SECRET).encode())
    headers = { 'Authorization': f'Basic {encoded_auth.decode()}', 'Content-Type': 'application/json'  }
    paypal_access_token = requests.request("POST", "https://api.sandbox.paypal.com/v1/oauth2/token", headers=headers, data='grant_type=client_credentials')
    paypal_access_token = paypal_access_token.json()
    paypal_access_token = paypal_access_token['access_token']

    if paypal_access_token:
        payload = json.dumps({
        "intent": "CAPTURE",
        "purchase_units": [ {
            "amount": {
                "currency_code": "USD",
                "value": total,
                "order_id": order_id
             } } ],
        "application_context": {
              "return_url": "http://127.0.0.1:8000/paypal/capturepayment/",
              "cancel_url": "https://example.com/cancel"
        } })
        headers = {"Content-Type": "application/json", "Authorization": 'Bearer '+paypal_access_token}
        create_order_response = requests.request("POST", "https://api-m.sandbox.paypal.com/v2/checkout/orders", headers=headers, data=payload)
        create_order_response = create_order_response.json()
        aprroval_link = create_order_response['links'][1]['href']
        paypal_order_id = create_order_response['id']
        capture_url = create_order_response['links'][3]['href']
        print(paypal_access_token)
    return Response(aprroval_link)

@csrf_exempt
@api_view(['POST'])
def capture_payment(request):
    global payer_email, paypal_data
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+paypal_access_token    }
    response = requests.request("POST", capture_url, headers=headers)
    response = response.json()
    status = response['status']
    paypal_account_id = response['payment_source']['paypal']['account_id']
    capture_payment_id = response['id']
    given_name = response['payer']['name']['given_name'] 
    surname = response['payer']['name']['surname']
    name = given_name  +  surname
    payer_email = response['payer']['email_address']     
    payer_id = response['payer']['payer_id']     
    payer_email = response['payer']['email_address']     
    country = response['payer']['address']['country_code']     
    currency = response['purchase_units'][0]['payments']['captures'][0]['amount']['currency_code']
    amount = response['purchase_units'][0]['payments']['captures'][0]['amount']['value']
    paypal_order_id = response['purchase_units'][0]['payments']['captures'][0]['id']
    create_time = response['purchase_units'][0]['payments']['captures'][0]['create_time']
    update_time = response['purchase_units'][0]['payments']['captures'][0]['update_time']
    
    receipt_id = requests.request("POST", "https://api-m.sandbox.paypal.com/v2/invoicing/generate-next-invoice-number", headers={ 'Authorization': 'Bearer '+paypal_access_token })
    receipt_id = receipt_id.json()
    receipt_id = receipt_id['invoice_number']
    if status == "COMPLETED":
        paypal_data = paypal_payment.objects.create(receipt_id=receipt_id, name= given_name + surname, user_id=user_id, email=payer_email, amount_received=amount, capture_payment_id=capture_payment_id, order_id = order_id, create_time = create_time, update_time = update_time, paypal_order_id = paypal_order_id, currency=currency, payer_id = payer_id )
        paypal_data.save()    
        order_data = Order.objects.filter(id=order_id).update(status='completed')
        subject, from_email, to = 'Receipt', settings.EMAIL_HOST_USER, email
        text_content = 'This is an important message.'
        html_content = '<p>Download your paypal payment receipt<br>http://127.0.0.1:8000/receipt/</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    else:
        return Response("Payment failed")
    order_details = Order.objects.filter(user_id=user_id).values('quantity','total','product')
    data = order_details, paypal_data
    return render(request, 'paypalreceipt.html', {"data": paypal_data})

@api_view(['GET']) 
def generate_pdf(request):
    # report = Order.objects.filter(user_id=user_id).values('quantity','total','product')
    template_path = 'paypalreceipt.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Receipt.pdf"'
    html = render_to_string(template_path, {'report': 123})
    pisaStatus = pisa.CreatePDF(html, dest=response)
    return response 

@csrf_exempt
@api_view(['GET'])
def mail(request):
    subject, from_email, to = 'Receipt', settings.EMAIL_HOST_USER, email
    text_content = 'This is an important message.'
    html_content = '<p>Download your paypal payment receipt<br>http://127.0.0.1:8000/receipt/</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return Response("mail sent")
       
@csrf_exempt
@api_view(['GET'])
def test(request):
    
    return Response(1123)