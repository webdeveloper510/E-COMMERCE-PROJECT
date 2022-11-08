from django.db import models


class stripe_payment(models.Model):
    name = models.CharField(max_length=90)
    user_id = models.CharField(max_length=90)
    order_id = models.CharField(max_length=90)
    email = models.EmailField(max_length = 150)
    amount_received = models.CharField(max_length=90)
    payment_intent_id = models.CharField(max_length=90)
    charge_id = models.CharField(max_length=90)
    amount_refund = models.CharField(max_length=90, null=True, blank=True)
    billing_details = models.TextField(max_length=350, null=True, blank=True)
    currency = models.CharField(max_length=90,null=True, blank=True)
    payment_method = models.TextField(max_length=350, null=True, blank=True)
    country = models.CharField(max_length=90, null=True, blank=True)
    city = models.CharField(max_length=90, null=True, blank=True)
    postal_code = models.CharField(max_length=90, null=True, blank=True)
    state = models.CharField(max_length=90, null=True, blank=True)
    status = models.CharField(max_length=90, null=True, blank=True)
    created_id = models.CharField(max_length=90, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class paypal_payment(models.Model):
    name = models.CharField(max_length=90)
    user_id = models.CharField(max_length=90, null=True, blank=True)
    order_id = models.CharField(max_length=90, null=True, blank=True)
    email = models.EmailField(max_length=90, null=True, blank=True)
    amount_received = models.CharField(max_length=90, null=True, blank=True)
    capture_payment_id = models.CharField(max_length=90)
    create_time = models.CharField(max_length=90)
    update_time = models.CharField(max_length=90, null=True, blank=True)
    paypal_order_id = models.TextField(max_length=350, null=True, blank=True)
    currency = models.CharField(max_length=90,null=True, blank=True)
    payer_id = models.TextField(max_length=350, null=True, blank=True)
    receipt_id = models.TextField(max_length=350, null=True, blank=True)

   
