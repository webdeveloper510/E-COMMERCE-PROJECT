from .models import Cart, DeliveryCost

class DeliveryCostHelper:

    def __init__(self, cart_items):
        self.cart_items = cart_items
        self.calculator = False
        self.number_of_deliveries = 0
        self.number_of_products = 0
        self.cost = 0

    def calculate_delivery_cost(self):
        try:
            self.calculator = DeliveryCost.objects.get(status='Active')

            delivery_categories = []

            for cart_item in self.cart_items:
                self.number_of_products += 1
                if cart_item.item.category.id not in delivery_categories:
                    delivery_categories.append(cart_item.item.category.id)
                    self.number_of_deliveries += 1

                self.cost = (self.calculator.cost_per_delivery * self.number_of_deliveries) + \
                            (self.calculator.cost_per_product * self.number_of_products) + self.calculator.fixed_cost

            return self.cost
        except Exception as e:
            print('Error when trying to getting coupon_discounts {0}'.format(str(e)))
            return False


class CartHelper:

    def __init__(self, user):
        self.user = user
        self.cart_base_total_amount = 0
        self.cart_final_total_amount = 0
        self.campaign_discount_amounts = []
        self.campaign_discount_amount = 0
        self.coupon_discount_amount = 0
        self.delivery_cost = 0
        self.cart_items = []
        self.discounts = {}
        self.checkout_details = {'products': [], 'total': [], 'amount': []}

    def prepare_cart_for_checkout(self):
        self.cart_items = Cart.objects.filter(user=self.user)

        if not self.cart_items:
            return False

        self.calculate_cart_base_total_amount()
        self.get_delivery_cost()
        

        return self.checkout_details

    def get_delivery_cost(self):
        delivery_helper = DeliveryCostHelper(cart_items=self.cart_items)
        self.delivery_cost = delivery_helper.calculate_delivery_cost()

    def calculate_cart_base_total_amount(self):
        for cart_item in self.cart_items:
            self.cart_base_total_amount += cart_item.item.price * cart_item.quantity

    



    