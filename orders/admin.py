# orders/admin.py
from django.contrib import admin
'''from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Allows to add extra order items inline

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at', 'updated_at', 'seller')  # Added seller
    list_filter = ('status', 'created_at', 'updated_at', 'seller')  # You can filter by these fields in the admin
    search_fields = ('user__username', 'status', 'seller__username')  # Allows searching by user and seller names
    inlines = [OrderItemInline]  # Inline display for OrderItems within Order

admin.site.register(Order, OrderAdmin)
'''