from rest_framework import serializers
from .models import SalesAnalytics, CustomReport, Product
from orders.models import Order
from cart.models import Cart
from django.db.models import Sum
from datetime import timedelta
from django.utils.timezone import now

class SalesAnalyticsSerializer(serializers.ModelSerializer):
    total_revenue = serializers.SerializerMethodField()
    growth_percentage = serializers.SerializerMethodField()
    most_viewed_product = serializers.StringRelatedField()

    class Meta:
        model = SalesAnalytics
        fields = ['total_revenue', 'growth_percentage', 'most_viewed_product', 'created_at']

    def get_total_revenue(self, obj):
        total_sales = Order.objects.aggregate(total_sales=Sum('total_amount'))
        return total_sales['total_sales'] if total_sales['total_sales'] else 0

    def get_growth_percentage(self, obj):
        total_sales = Order.objects.aggregate(total_sales=Sum('total_amount'))
        total_revenue = total_sales['total_sales'] if total_sales['total_sales'] else 0
        growth_last_month = Order.objects.filter(
            created_at__gte=now() - timedelta(days=30)
        ).aggregate(last_month_sales=Sum('total_amount'))['last_month_sales'] or 0
        return ((total_revenue - growth_last_month) / growth_last_month) * 100 if growth_last_month else 0

class CustomReportSerializer(serializers.ModelSerializer):
    data = serializers.JSONField()

    class Meta:
        model = CustomReport
        fields = ['report_name', 'start_date', 'end_date', 'created_at', 'data']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'stock_quantity']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_amount', 'status', 'created_at']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'order']
