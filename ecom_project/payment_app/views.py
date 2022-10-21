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

#stripe

stripe.api_key = settings.API_SECRET_KEY

#create card token to use it in charge and name to create customer id
@csrf_exempt
@api_view(['POST'])
def card_token(request):
            global card_id, card_token, name 
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
            print(total)
            
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
                charge_data.save()
                if status == "succeeded":
                    body = receipt_url
                    data = {
                        'subject':'Stripe Payment Receipt',
                        'body':body,
                        'to_email': email
                    }
                    Util.send_email(data)
                    print(body)
                    order_data = Order.objects.filter(user_id=user_id).update(status='completed')
            return Response(card_id)      



#paypal
@csrf_exempt
@api_view(['POST'])
def get_paypal_access_token(request):
    global total, paypal_access_token, aprroval_link, capture_url, paypal_order_id, user_id, order_id
    
    user_id = request.data.get('user_id')
    order_id = request.data.get('order_id')
    total = request.data.get('total')
    name = request.data.get('name')
    email = request.data.get('email')

    url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    payload = 'grant_type=client_credentials'
    encoded_auth = base64.b64encode((settings.CLIENT_ID + ':' + settings.CLIENT_SECRET).encode())
    headers = {
      'Authorization': f'Basic {encoded_auth.decode()}',
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    access_token_r = requests.request("POST", url, headers=headers, data=payload)
    access_token_r = access_token_r.json()
    paypal_access_token = access_token_r['access_token']

    if paypal_access_token ==  paypal_access_token:
        url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
        payload = json.dumps({
        "intent": "CAPTURE",
        "purchase_units": [
            {
            "amount": {
                "currency_code": "USD",
                "value": total,
                "order_id": order_id
             }
            }
        ],
        "application_context": {
            "return_url": "https://example.com/return",
            "cancel_url": "https://example.com/cancel"
        }
        })
        headers = {"Content-Type": "application/json", "Authorization": 'Bearer '+paypal_access_token}
        create_order_response = requests.request("POST", url, headers=headers, data=payload)
        create_order_response = create_order_response.json()
        aprroval_link = create_order_response['links'][1]['href']
        paypal_order_id = create_order_response['id']
        capture_url = create_order_response['links'][3]['href']
        print(paypal_access_token)
    return Response(aprroval_link)


@csrf_exempt
@api_view(['POST'])
def capture_payment(request):
    global payer_email
    headers = {'Content-Type': 'application/json',
    'Authorization': 'Bearer '+paypal_access_token    }
    response = requests.request("POST", capture_url, headers=headers)
    response = response.json()
    status = response['status']
    paypal_account_id = response['payment_source']['paypal']['account_id']
    capture_payment_id = response['id']
    given_name = response['payer']['name']['given_name'] 
    surname = response['payer']['name']['surname']
    name = given_name  +  surname
    email = response['payer']['email_address']     
    payer_id = response['payer']['payer_id']     
    payer_email = response['payer']['email_address']     
    country = response['payer']['address']['country_code']     
    currency = response['purchase_units'][0]['payments']['captures'][0]['amount']['currency_code']
    amount = response['purchase_units'][0]['payments']['captures'][0]['amount']['value']
    create_time = response['purchase_units'][0]['payments']['captures'][0]['create_time']
    update_time = response['purchase_units'][0]['payments']['captures'][0]['update_time']
    # paypal_order_id= paypal_order_id
    print("account id is --", paypal_account_id)
    if status == "COMPLETED":
        body = "Your order has been confirmed"
        data = {
                'subject':'Paypal Payment Receipt',
                'body':body,
                'to_email': "gurpreet@codenomad.net" 
            }
        Util.send_email(data)
        paypal_data = paypal_payment.objects.create( name = name, user_id = user_id, email = email,
            amount_received = amount, capture_payment_id = capture_payment_id,
            create_time = create_time, update_time = update_time,
            country = country, currency = currency, payer_id = payer_id )
        paypal_data.save()
    
    else:
        return Response("Payment failed")
    return Response(response)

from time import gmtime, strftime

@csrf_exempt
@api_view(['GET'])
def transaction(request):
    # time = str(datetime.datetime.now())
    # showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    # showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    # print(time, showtime)
    URL = "https://api-m.sandbox.paypal.com/v1/reporting/transactions?fields=transaction_info,payer_info,auction_info,cart_info,&start_date=2022-10-19T01:05:00.999Z&end_date=2022-10-20T11:40:00.999Z"
    headers = {'Content-Type': 'application/json',
    'Authorization': 'Bearer '+paypal_access_token    }
    response = requests.request("GET", URL, headers=headers)
    response = response.json()
    i = 0
    for x in response:
        transaction_info = response['transaction_details'][i]['transaction_info']
        payer_info = response['transaction_details'][i]['payer_info']
        cart_info = response['transaction_details'][i]['cart_info']
        payer_name = payer_info['payer_name']
        i = i+1
        print(i, cart_info)
        if payer_name:
            transaction_email = payer_info['email_address']
            account_id = payer_info['account_id']
            print(transaction_email)
            print(account_id, "info", payer_info, cart_info)

        #     if transaction_email == payer_email:
        #         details = {transaction_info['transaction_id'],transaction_info['paypal_reference_id'],
        #               transaction_info['paypal_reference_id_type'],transaction_info['transaction_event_code'],
        #               transaction_info['transaction_initiation_date'],transaction_info['transaction_updated_date'],
        #               transaction_info['transaction_amount'],payer_info,response['cart_info']}
        #         print(details)
        #         break
    return Response(response)

@csrf_exempt
@api_view(['GET'])
def test(request):
    
         
    return Response({123})

from paypalrestsdk import CreditCard
from paypalrestsdk import Payment
import paypalrestsdk

def card_payemnt(request):
    try:
        paypalrestsdk.configure({
            "mode": "sandbox",  # sandbox or live
            'client_id' : settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
        })

        credit_card = CreditCard({
            "type": "visa",
            "number": "4024007185826731",
            "expire_month": "12",
            "expire_year": "2022",
            "cvv2": "874",
            "first_name": "Joe",
            "last_name": "Shopper",
        })

        if credit_card.create():
            print("CreditCard[%s] created successfully" % (credit_card.id ))
            return Response('good')
        else:
            print("Error while creating CreditCard:")
            print(credit_card.error)
    except Exception as e:
        print(str(e))
        return Response("Hello")

def credit_card_payment(request):
            paypalrestsdk.configure({
                "mode": "sandbox",  # sandbox or live
               'client_id' : settings.CLIENT_ID,
               'client_secret': settings.CLIENT_SECRET,
            })
            payment = paypalrestsdk.Payment(
                {
                    "intent": "sale",
                    "payer": {
                        "payment_method": "credit_card",
                        "funding_instruments": [
                            {
                                "credit_card_token": {
                                    "credit_card_id": "CARD-7MH68586JW7132142LXWASJI",

                                }
                            }]
                    },
                    "transactions": [
                        {
                            "amount": {
                                "total": "6.70",
                                "currency": "USD"
                            },
                            "description": "Payment by vaulted credit card."
                        }]
                }
            )
            if payment.create():
                print(payment.id)

                print("Payment created successfully")
            else:
                print(payment.error)