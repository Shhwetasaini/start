# cart/admin.py
from django.contrib import admin
'''from .models import Cart, CartItem
from orders.models import Order  # Import Order model to use in CartAdmin

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at', 'get_order', 'get_status', 'is_abandoned')
    inlines = [CartItemInline]  # Inline display for CartItems within Cart

    def get_order(self, obj):
        order = obj.get_order()
        return order.id if order else None
    get_order.short_description = 'Order ID'

    def get_status(self, obj):
        order = obj.get_order()
        return order.status if order else 'No Order'
    get_status.short_description = 'Order Status'

    def is_abandoned(self, obj):
        # Logic to determine if the cart is abandoned (not converted to an order)
        if not obj.get_order():
            return "Abandoned"
        return "Converted"
    is_abandoned.short_description = 'Abandoned Cart'

admin.site.register(Cart, CartAdmin)
'''