from django.db import models
from products.models import Product
from django.conf import settings
#from cart.models import Cart

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="orders_orders", on_delete=models.CASCADE)
    cart = models.ForeignKey('cart.Cart', on_delete=models.CASCADE, default=1)  # Use string reference here
    address = models.TextField()
    payment_method = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='Pending')
    

    def __str__(self):
        return f"Order {self.id} for {self.user}"

    def get_items(self):
        return self.items_orders.all()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items_orders", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items_orders", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
