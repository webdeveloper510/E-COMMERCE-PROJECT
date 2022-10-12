from django.db import models

class stripe_Product(models.Model):
    name = models.CharField(max_length=100)
    stripe_product_id = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Price(models.Model):
    product = models.ForeignKey(stripe_Product, on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

#paypal
class order(models.Model):
    pass

class stripe_charge(models.Model):
    amount = models.CharField(max_length=90, null=True, blank=True)
    order = models.CharField(max_length=90, null=True, blank=True)
    customer_id = models.CharField(max_length=90, null=True, blank=True)
    name = models.CharField(max_length=90, null=True, blank=True)
    phone = models.CharField(max_length=90, null=True, blank=True)
    country = models.CharField(max_length=90, null=True, blank=True)
    city = models.CharField(max_length=90, null=True, blank=True)
    postal_code = models.CharField(max_length=90, null=True, blank=True)
    state = models.CharField(max_length=90, null=True, blank=True)
    payment_method = models.CharField(max_length=90, null=True, blank=True)
    status = models.CharField(max_length=90, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

