from django.conf import settings
from django.db import models
from products.models import Product
from orders.models import Order, OrderItem

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="cart_user", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_order(self):
        try:
            return Order.objects.filter(cart=self).first()
        except Order.DoesNotExist:
            return None

    def __str__(self):
        return f"Cart {self.id} for {self.user}"

class CartItem(models.Model):
    cart = models.ForeignKey('cart.Cart', related_name="items_cart", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="cart_items_product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
