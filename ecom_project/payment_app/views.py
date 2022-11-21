from ecom_project.library import *
from product_app.models import *
from payment_app.models import *
from account_app.serializers import UserProfileSerializer

#stripe
stripe.api_key = settings.API_SECRET_KEY

#create card token to use it in charge and name to create customer id
class StripePaymentViewSet(viewsets.ViewSet):
    @csrf_exempt 
    @action(detail=False, permission_classes=[IsAuthenticated], methods=['POST'])        
    def payment(self, request, format=None):
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
        serializer=UserProfileSerializer(request.user)
        if user_id == serializer.data['id']:
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
                if status == "succeeded":
                    order_data = Order.objects.filter(id=order_id).update(status='completed')
                    order_details = Order.objects.filter(id=order_id).values('total','item','street_address','apartment','city','state','name')
                    created_id = payment_intent['charges']['data'][0]['created']
                    item = order_details[0]['item']
                    my_dict = ast.literal_eval(item)
                    item_list = []
                    for items in my_dict:
                        item_list.append(items)
                    showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    context = {'receipt_id':created_id, 'order_id':order_id,'item':item_list,
                                'date': showtime, 'order_details': order_details}
                    charge_data = stripe_payment.objects.create(name=payment_intent['charges']['data'][0]['metadata']['name'], 
                    user_id = payment_intent['charges']['data'][0]['metadata']['user_id'], order_id = payment_intent['charges']['data'][0]['metadata']['order_id'],
                    amount_received=  payment_intent['charges']['data'][0]['amount_captured'], payment_intent_id= payment_intent['id'], 
                    billing_details = payment_intent['charges']['data'][0]['billing_details']['address'], receipt_id = payment_intent['charges']['data'][0]['created'])
                    charge_data.save()
#sending email for payment receipt
                    template = get_template('stripereceipt.html')
                    html  = template.render(context)
                    result = BytesIO()
                    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
                    pdf = result.getvalue()
                    filename = 'Receipt.pdf'
                    to_emails = [serializer.data['email']]
                    subject = "Payment Recipt from Frame-Art"
                    email = EmailMessage(subject, "Payment Recipt from Frame-Art", from_email=settings.EMAIL_HOST_USER, to=to_emails)
                    email.attach(filename, pdf, "application/pdf")
                    email.send(fail_silently=False)
                    return Response("Please check your email for payment confirmation")
                else:
                    return Response("Payment failed")   
            return Response("Payment completed")
        else:
            return Response("Order is not found.")

#paypal
class PaypalPaymentViewSet(viewsets.ViewSet):
    @csrf_exempt 
    @action(detail=False, permission_classes=[IsAuthenticated], methods=['POST'])
    def create_order(self, request, *args, **kwargs):
        global paypal_access_token
        user_id = request.data.get('user_id')
        order_id = request.data.get('order_id')
        total = request.data.get('total')
        name = request.data.get('name')
        serializer=UserProfileSerializer(request.user)
        email = serializer.data['email']
        if user_id == serializer.data['id']:
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
                    "return_url": "http://127.0.0.1:5500/templates/thankyou.html",
                    "cancel_url": "https://example.com/cancel"
                } })
                headers = {"Content-Type": "application/json", "Authorization": 'Bearer '+paypal_access_token}
                create_order_response = requests.request("POST", "https://api-m.sandbox.paypal.com/v2/checkout/orders", headers=headers, data=payload)
                create_order_response = create_order_response.json()
                aprroval_link = create_order_response['links'][1]['href']
                paypal_order_id = create_order_response['id']
                capture = create_order_response['links'][3]['href']
                capture_data = capture_paypal_payment.objects.create(capture_url=capture, status="pending", order_id=order_id, user_id= user_id)
                capture_data.save()
                print(paypal_access_token)
        return Response(aprroval_link)
    
    @csrf_exempt 
    @action(detail=False, permission_classes=[IsAuthenticated], methods=['POST'])
    def capture_payment(self, request, *args, **kwargs):
        obj = capture_paypal_payment.objects.filter(status="pending").first()
        capture_url = getattr(obj, 'capture_url')
        capture_url_id = int(getattr(obj, 'id'))
        order_id = int(getattr(obj, 'order_id'))
        user_id = int(getattr(obj, 'user_id'))
        serializer=UserProfileSerializer(request.user)
        print(user_id, serializer.data['id'])
        if user_id == serializer.data['id']:
#capture payment 
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+paypal_access_token}
            response = requests.request("POST", capture_url, headers=headers)
            response = response.json()
            if 'status' in response: 
                paypal_account_id = response['payment_source']['paypal']['account_id']
                paypal_order_id = response['id']
                given_name = response['payer']['name']['given_name'] 
                surname = response['payer']['name']['surname']
                name = given_name  +  surname
                payer_email = response['payer']['email_address']     
                payer_id = response['payer']['payer_id']     
                payer_email = response['payer']['email_address']     
                country = response['payer']['address']['country_code']     
                currency = response['purchase_units'][0]['payments']['captures'][0]['amount']['currency_code']
                amount = response['purchase_units'][0]['payments']['captures'][0]['amount']['value']
                capture_payment_id = response['purchase_units'][0]['payments']['captures'][0]['id']
                create_time = response['purchase_units'][0]['payments']['captures'][0]['create_time']
                update_time = response['purchase_units'][0]['payments']['captures'][0]['update_time']
#creating invoice no as receipt id        
                receipt_id = requests.request("POST", "https://api-m.sandbox.paypal.com/v2/invoicing/generate-next-invoice-number", headers={ 'Authorization': 'Bearer '+paypal_access_token })
                receipt_id = receipt_id.json()
                receipt_id = receipt_id['invoice_number']
                if str(response['status']) == "COMPLETED":
                    paypal_data = paypal_payment.objects.create(receipt_id=receipt_id, name= name, user_id=user_id, amount_received=amount, capture_payment_id=capture_payment_id, order_id = order_id, create_time = create_time, update_time = update_time, paypal_order_id = paypal_order_id, currency=currency, payer_id = payer_id )
                    paypal_data.save()    
                    order_data = Order.objects.filter(id=order_id).update(status='completed')
                    capture_paypal_payment_data = capture_paypal_payment.objects.filter(id=capture_url_id).update(status="completed")
                    order_details = Order.objects.filter(id=order_id).values('item','street_address','apartment','city','state','name')
                    item = order_details[0]['item']
                    my_dict = ast.literal_eval(item)
                    item_list = []
                    for items in my_dict:
                        item_list.append(items)
                    showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
#context           
                    context= {'paypal_data': paypal_data, 'name':order_details[0]['name'], 'order_details': order_details, 'date': showtime, 'item':item_list }
#pdf receipt            
                    template = get_template('paypalreceipt.html')
                    html  = template.render(context)
                    result = BytesIO()
                    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
                    pdf = result.getvalue()
                    filename = 'Receipt.pdf'
                    to_emails = [serializer.data['email']]
                    subject = "Payment Recipt from Frame-Art"
                    email = EmailMessage(subject, "Payment Recipt from Frame-Art", from_email=settings.EMAIL_HOST_USER, to=to_emails)
                    email.attach(filename, pdf, "application/pdf")
                    email.send(fail_silently=False)
                    return Response("Please check your email for payment confirmation")
                return Response("payment completed")
#payment not done
        if 'details' in response:
            value = response['details'][0]['issue'] 
            if value == "ORDER_ALREADY_CAPTURED":
                capture_paypal_payment_data = capture_paypal_payment.objects.filter(id=capture_url_id).update(status="completed")
                return Response("Order already captured")
            elif value == "ORDER_NOT_APPROVED":
                obj = capture_paypal_payment.objects.get(id=capture_url_id).delete()
                return Response("ORDER_NOT_APPROVED")
        return Response("payment completed")

@csrf_exempt
@api_view(['GET'])
def test(request):
    url = "https://api-m.sandbox.paypal.com/v2/payments/captures/9SX25532EE7624132"
    payload={}
    headers = {
    'Authorization': 'Bearer A21AAJg3AYhuDOdrSTT-7Weh4wY2KUHbFYgV4UHaxzQY_1II0zpcSHCO_glPIRYx3FfncuTUd2ykpAEhk_9G625Tyjw4EUKuw'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return Response(response.json())