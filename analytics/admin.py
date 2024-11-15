# admin.py in analytics app
from django.contrib import admin
'''from django.db.models import Sum
from products.models import Product
from orders.models import Order
from .models import CustomReport, SalesAnalytics

class SalesAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('total_revenue', 'growth_percentage', 'most_viewed_product')

    def total_revenue(self, obj):
        total_sales = Order.objects.aggregate(total_sales=Sum('total_amount'))
        return total_sales['total_sales'] if total_sales['total_sales'] else 0

    def growth_percentage(self, obj):
        return obj.calculate_growth_percentage()

    def most_viewed_product(self, obj):
        top_product = Product.objects.values('id').annotate(view_count=Sum('views')).order_by('-view_count').first()
        if top_product:
            return top_product.get('name', "N/A")
        return "N/A"
    most_viewed_product.short_description = 'Most Viewed Product'

class CustomReportAdmin(admin.ModelAdmin):
    list_display = ('report_name', 'start_date', 'end_date', 'created_at')
    list_filter = ('start_date', 'end_date')

# Registering models with their admin classes
admin.site.register(SalesAnalytics, SalesAnalyticsAdmin)
admin.site.register(CustomReport, CustomReportAdmin)
'''