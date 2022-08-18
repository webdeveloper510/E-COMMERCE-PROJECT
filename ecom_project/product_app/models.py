
from django.db import models
from account_app.models import *
import datetime
from ecom_project import settings
from django.db.models import F, Sum

class Category(models.Model):
      name = models.CharField(max_length=250)
  
      def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=500, null=False, blank= False)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Variant_type(models.Model):
    type = models.CharField(max_length=250)
    
    def __str__(self):
        return self.type
        
class Variant(models.Model):
        variant_name = models.CharField(max_length=250)
        variant_type = models.ForeignKey(Variant_type, on_delete=models.CASCADE)

        def __str__(self):
         return "{} - {} -".format(self.variant_name,self.variant_type)


class ProductAttribute(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant_name = models.ForeignKey(Variant, on_delete=models.CASCADE)
    variant_type = models.ForeignKey(Variant_type, on_delete=models.PROTECT, blank=True, null=True)
    price = models.DecimalField(max_digits=25, decimal_places=2)

    def __str__(self):
        return "{} - {} -".format(self.category,self.product,self.variant_name,
                                  self.variant_type,self.price)


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ManyToManyField(ProductAttribute)
    price = models.DecimalField(max_digits=25, decimal_places=2)
    

class Price(models.Model):
    type_id = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=25, decimal_places=2)
    DisplayFields = ['id', 'type_id', 'value', 'total']
    
    @property
    def price(self):
        total = Price.objects.annotate(F('type_id') * F('price'))
        return total

class Types(models.Model):
        variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)
        price = models.CharField(max_length=50)
    

        

'''
    price = models.FloatField(null=False, blank= False, default=30.30)
    length = models.DecimalField(default=30.30, max_digits=5, decimal_places=1)
    width = models.DecimalField(default=30.30, max_digits=5, decimal_places=1)
    depth = models.DecimalField(default=30.30, max_digits=5, decimal_places=1)
    paper = models.CharField(max_length=90)
    coating = models.CharField(max_length=90)
    printed_sides = models.CharField(max_length=90)
    quantity = models.IntegerField(default=1)
   
    def __str__(self):
        return self.name
''' 
class Variant_type(models.Model):
        type = models.CharField(max_length=250)
        
class Variant(models.Model):
        name = models.CharField(max_length=250)
        variant_type = models.ForeignKey(Variant_type, on_delete=models.CASCADE)

        def __str__(self):
         return self.name
class Types(models.Model):
        variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)
        price = models.CharField(max_length=50)

''' 
class Attribute(models.Model):
        variant_type = models.CharField( max_length=250)
        variant=models.CharField(max_length=250)
        price=models.CharField(max_length=240)


TITLE_CHOICES = [
    ('Height', 'height' ),
    ('Length', 'length'),
    ('Printing-sides', (
            ('Printing-sides_All', 'printing-sides_all'),
            ('Printing-sides_Left', 'printing-sides_left'),
        )
    ),
]


class Variants(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    type = models.CharField(max_length=250, choices=TITLE_CHOICES)
    price = models.FloatField(null=False, blank= False, default=30.30)
    value = models.CharField(max_length=250)
    
        
class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return self.updated_at




    @property
    def get_total(self):
        total_price  = self.price * self.value
        return total_price

'''

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    type_id = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=25, decimal_places=2)

    '''
    quantity = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
'''
    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.user,
                                               self.type_id,
                                               self.value,
                                              )

class DeliveryCost(models.Model):
    cost_per_delivery = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    cost_per_product = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    fixed_cost = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {} - {} - {}".format(self.cost_per_delivery,
                                                    self.cost_per_product,
                                                    self.fixed_cost,
                                                    self.created_at,
                                                    self.updated_at)




'''
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    length = models.DecimalField(default=30.30, max_digits=5, decimal_places=1)
    height = models.DecimalField(default=30.30, max_digits=5, decimal_places=1)
    paper = models.CharField(max_length=90)
    coating = models.CharField(max_length=90)
    printed_sides = models.CharField(max_length=90)
    quantity = models.IntegerField(default=1)
    paid = models.BooleanField(default=False)
   
    price = models.FloatField(null=False, blank= False, default=30.30)
    value = models.CharField(max_length=250)
    quantity = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user} - {str(self.id)}'

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
 


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='order_items')
    price = models.IntegerField()
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
'''
