from http.client import HTTPResponse
from xmlrpc.client import ResponseError
import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
import uuid
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from product_app.views import *
from base64 import b64encode
import base64
import requests
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import requests
import json
from django.views.decorators.csrf import csrf_exempt

#stripe
stripe.api_key = settings.API_SECRET_KEY

# create a stripe customer
@csrf_exempt
@api_view(['POST'])
def home(request):
    global customer_id
    try:
        # description = request.data.get('description')
        # name = request.data.get('name')
        email = request.data.get('email')

        data = stripe.Customer.create(
            # description= description,
            # name= name,
            email= email,
        )
    except Exception as error:
        print("error is",error)

    customer_id = data['id']
    return Response(data)

#create card token  
@csrf_exempt
@api_view(['POST'])
def card_token(request):
        global card_id, card_token
        number = request.data.get('number')
        exp_month = request.data.get('exp_month')
        exp_year = request.data.get('exp_year')
        cvc = request.data.get('cvc')

        print(number,exp_month, exp_year, cvc )
        data = stripe.Token.create(
        card={
            "number": number,
            "exp_month": exp_month,
            "exp_year": exp_year,
            "cvc": cvc,
        },
        )
        card_token = data['id']
        card_id = data['card']['id']
        return Response({card_token, card_id})

#create card source
@csrf_exempt
@api_view(['POST'])
def card(request):
        print(customer_id, card_token)
        data = stripe.Customer.create_source(
             customer_id,
            source = card_token
            )
        return Response(data)

#Payment intent
@csrf_exempt
@api_view(['POST'])
def payment_intent(request):
        payment_intent = stripe.PaymentIntent.create(
            customer = 'cus_MZMngHOpJ4WDLz',
            amount= 4000,
            currency="usd",
            payment_method_types=["card"],
            payment_method = "card_1LrJUbJTvBqbiOKnTQunPNtn",
            confirmation_method = 'automatic',
            confirm=True,
            # source = 'card_1LrJUbJTvBqbiOKnTQunPNtn'
            )
        return Response(payment_intent)

  
@csrf_exempt
@api_view(['POST'])
def charge(request):
        data = stripe.Charge.create(
            amount= 3000,
            currency="usd",
            source= card_token,
            description="My First Test Charge",
            )
        return Response(data)



#paypal
client_id = settings.CLIENT_ID
client_secret = settings.CLIENT_SECRET

@csrf_exempt
@api_view(['POST'])
def tok(request):
    global paypal_access_token
    if request.method == 'POST':
        url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
        payload='grant_type=client_credentials&ignoreCache=true&return_authn_schemes=true&return_client_metadata=true&return_unconsented_scopes=true'
        headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic QVpiU2JlczFIbHdtaUktN3dHT05KS0lBOFhUcHRSSXhrS3JaMUhTaGE3bVZTdEJoVHI5OE9WaWZKeEVlMmRZak90eE5vM2xhSGxNRnplZzE6RVBhZU1TaVF0WjIyT1dPZDR5OGNERE9TaDNkU2dLbHZFN2tXWGRjb3dkTzBJYkZmNF8xX2lIbHJOT1FuU2plOHZMNktmMWxoeFdtT2M0ZjY=',
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response = response.json()
        paypal_access_token = response['access_token']
    return Response(response)


@csrf_exempt
@api_view(['POST'])
def create_order(request):
    if request.method == 'POST':
        url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
        payload = json.dumps({
        "intent": "CAPTURE",
        "purchase_units": [
            {
            "items": [
                {
                "name": "T-Shirt",
                "description": "Green XL",
                "quantity": "1",
                "unit_amount": {
                    "currency_code": "USD",
                    "value": "200.00"
                }
                }
            ],
            "amount": {
                "currency_code": "USD",
                "value": "200.00",
                "breakdown": {
                "item_total": {
                    "currency_code": "USD",
                    "value": "200.00"
                }
                }
            }
            }
        ],
        "application_context": {
            "return_url": "https://example.com/return",
            "cancel_url": "https://example.com/cancel"
        }
        })
        headers = {
        'Content-Type': 'application/json',
        'Prefer': 'return=representation',
        'PayPal-Request-Id': 'b0b38785-bd3a-4394-ac28-2ac500419f2b',
        'PayPal-Client-Metadata-Id': '',
        'PayPal-Partner-Attribution-Id': 'TEST_ATTRIBUTION_ID',
        'PayPal-Auth-Assertion': '',
        'Authorization': 'Bearer A21AAJSktKFofgIKKJFst_biyfcwF9XUwhmuJ1CB0wYf31vgprirqMJvIMydZjFrc5Zu3R9gLVzHCJrDQ0DOU67GSxjPVbUyw'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        r = requests.request("POST", url, headers=headers, data=payload)
        response = r.json()
        # aprroval_link = response['links'][1]['href']
        # print(aprroval_link)
    return Response(response)


@csrf_exempt
@api_view(['POST'])
def capture_payment(request):
    url = "https://api-m.sandbox.paypal.com/v2/checkout/orders/70203260R3854615X/capture"
    payload={}
    headers = {
    'Content-Type': 'application/json',
    'Prefer': 'return=representation',
    'PayPal-Request-Id': '927d4d86-5113-4486-a3ea-59b012f01151',
    'Authorization': 'Bearer A21AAINAnFQq7GhwUBxdOMrQ1PM1rsb5Co6YBmgdM20EYZu7KH0d_PnnjfWqxACoDp_FPC4Ps7oWv8TSvuU379oSjBXPDrmIA'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return Response(123)


