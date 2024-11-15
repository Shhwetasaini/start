from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='get_items', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'address', 'payment_method', 'total_amount', 'items', 'status', 'created_at', 'updated_at']
