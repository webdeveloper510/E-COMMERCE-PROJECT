from django.contrib import admin
from .models import *

admin.site.register(stripe_payment)
admin.site.register(paypal_payment)