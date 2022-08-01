from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from .models import *

@receiver(valid_ipn_received)
def valid_ipn_signal(sender, **kwargs):
    print('Ipn valid')
    ipn = sender
    if ipn.payment_status == 'Completed':
        order.objects.create()
        
@receiver(invalid_ipn_received)
def invalid_ipn_signal(sender, **kwargs):
    print('Ipn invalid')
    ipn = sender
    if ipn.payment_status == 'Completed':
        order.objects.create()