from django.db import models
from products.models import Product
from orders.models import Order
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta

class SalesAnalytics(models.Model):
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    growth_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    most_viewed_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_growth_percentage(self):
        total_sales = Order.objects.aggregate(total_sales=Sum('total_amount'))
        total_revenue = total_sales['total_sales'] if total_sales['total_sales'] else 0
        
        growth_last_month = Order.objects.filter(
            created_at__gte=now() - timedelta(days=30)
        ).aggregate(last_month_sales=Sum('total_amount'))['last_month_sales'] or 0

        if growth_last_month:
            return ((total_revenue - growth_last_month) / growth_last_month) * 100
        return 0

    def __str__(self):
        return f"Sales Analytics: {self.total_revenue} at {self.created_at}"

    '''def update_sales_analytics():
        total_sales = Order.objects.aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
        last_month_sales = Order.objects.filter(
            created_at__gte=now() - timedelta(days=30)
        ).aggregate(last_month_sales=Sum('total_amount'))['last_month_sales'] or 0
    
        growth_percentage = ((total_sales - last_month_sales) / last_month_sales * 100) if last_month_sales else 0
    
        most_viewed_product = Product.objects.annotate(
            view_count=Count('cart_items_product')
        ).order_by('-view_count').first()
    
    # Create a new SalesAnalytics record
        SalesAnalytics.objects.create(
            total_revenue=total_sales,
            growth_percentage=growth_percentage,
            most_viewed_product=most_viewed_product
    )'''


class CustomReport(models.Model):
    report_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    data = models.JSONField()

    def __str__(self):
        return f"{self.report_name} ({self.start_date} to {self.end_date})"
