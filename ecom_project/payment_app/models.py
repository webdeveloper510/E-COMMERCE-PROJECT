from django.db import models

class stripe_payment(models.Model):
    name = models.CharField(max_length=90)
    receipt_id = models.CharField(max_length=90)
    user_id = models.CharField(max_length=90)
    order_id = models.CharField(max_length=90)
    amount_received = models.CharField(max_length=90)
    payment_intent_id = models.CharField(max_length=90)
    billing_details = models.TextField(max_length=350, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class paypal_payment(models.Model):
    name = models.CharField(max_length=90)
    user_id = models.CharField(max_length=90, null=True, blank=True)
    order_id = models.CharField(max_length=90, null=True, blank=True)
    paypal_order_id = models.TextField(max_length=350, null=True, blank=True)
    amount_received = models.CharField(max_length=90, null=True, blank=True)
    capture_payment_id = models.CharField(max_length=90)
    currency = models.CharField(max_length=90,null=True, blank=True)
    receipt_id = models.TextField(max_length=350, null=True, blank=True)
    create_time = models.CharField(max_length=90)
    update_time = models.CharField(max_length=90, null=True, blank=True)
    
class capture_paypal_payment(models.Model):
    user_id = models.CharField(max_length=90, null=True, blank=True)
    order_id = models.CharField(max_length=90, null=True, blank=True)
    capture_url = models.CharField(max_length=250)
    status = models.CharField(max_length=150)
