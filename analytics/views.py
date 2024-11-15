from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum
from datetime import datetime, timedelta
from django.utils.timezone import now
from products.models import Product
from cart.models import Cart
from orders.models import Order
from .models import CustomReport, SalesAnalytics
from .serializers import SalesAnalyticsSerializer, CustomReportSerializer
from django.db import models


class SalesAnalyticsView(APIView):
    
    def get(self, request):
        
        total_revenue = Order.objects.aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
        last_month_sales = Order.objects.filter(
            created_at__gte=now() - timedelta(days=30)
        ).aggregate(last_month_sales=Sum('total_amount'))['last_month_sales'] or 0
        growth_percentage = ((total_revenue - last_month_sales) / last_month_sales) * 100 if last_month_sales else 0

        most_viewed_product = Product.objects.annotate(
            view_count=Count('cart_items_product')
        ).order_by('-view_count').first()

        return Response({
            'total_revenue': total_revenue,
            'growth_percentage': growth_percentage,
            'most_viewed_product': most_viewed_product.name if most_viewed_product else None
        })


class UserBehaviorAnalyticsView(APIView): 
    def get(self, request):
        most_viewed_products = Product.objects.annotate(
            view_count=Count('cart_items_product')
        ).order_by('-view_count')[:10]

        abandoned_carts = Cart.objects.filter(
            created_at__lt=now() - timedelta(days=7),
            order__isnull=True
        )
        
        total_orders = Order.objects.count()
        total_carts = Cart.objects.count()
        conversion_rate = (total_orders / total_carts) * 100 if total_carts else 0

        data = {
            'most_viewed_products': [
                {'product_name': product.name, 'view_count': product.view_count}
                for product in most_viewed_products
            ],
            'abandoned_carts': [
                {'cart_id': cart.id, 'created_at': cart.created_at} for cart in abandoned_carts
            ],
            'conversion_rate': conversion_rate
        }
        return Response(data)

class InventoryManagementView(APIView): 
    def get(self, request):
        low_stock_products = Product.objects.filter(stock_quantity__lt=10)
        
        data = {
            'low_stock_products': [
                {'product_name': product.name, 'stock_quantity': product.stock_quantity}
                for product in low_stock_products
            ]
        }
        return Response(data)

class GenerateCustomReportView(APIView):
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        try:
            if start_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).date()
        if not end_date:
            end_date = datetime.now().date()

        total_sales_in_range = Order.objects.filter(
            created_at__gte=start_date, created_at__lte=end_date
        ).aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0

        total_sales_in_range = float(total_sales_in_range)

        most_viewed_products_in_range = Product.objects.annotate(
            view_count=Count('cart_items_product')
        ).order_by('-view_count')[:10]

        report_data = {
            'total_sales': total_sales_in_range,
            'most_viewed_products': [
                {'product_name': product.name, 'view_count': product.view_count}
                for product in most_viewed_products_in_range
            ]
        }

        custom_report = CustomReport.objects.create(
            report_name="Sales and User Behavior Report",
            start_date=start_date,
            end_date=end_date,
            data=report_data
        )

        serializer = CustomReportSerializer(custom_report)

        return Response({
            'report_id': custom_report.id,
            'message': 'Report generated successfully',
            'data': serializer.data
        })

class AnalyticsView(APIView): 
    def get(self, request):
        total_sales = Order.objects.aggregate(total_sales=Sum('total_amount'))
        total_revenue = total_sales['total_sales'] if total_sales['total_sales'] else 0

        most_viewed_products = Product.objects.annotate(
            view_count=Count('cart_items_product')
        ).order_by('-view_count')[:10]

        abandoned_carts = Cart.objects.filter(
            created_at__lt=now() - timedelta(days=7),
            order__isnull=True
        )

        low_stock_products = Product.objects.filter(stock_quantity__lt=10)
        
        data = {
            'total_sales': total_revenue,
            'most_viewed_products': [
                {'product_name': product.name, 'view_count': product.view_count}
                for product in most_viewed_products
            ],
            'abandoned_carts': [
                {'cart_id': cart.id, 'created_at': cart.created_at} for cart in abandoned_carts
            ],
            'low_stock_products': [
                {'product_name': product.name, 'stock_quantity': product.stock_quantity}
                for product in low_stock_products
            ]
        }
        return Response(data)
