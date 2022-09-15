from django.contrib import admin
from .models import *

admin.site.register(stripe_Product)
admin.site.register(Price)