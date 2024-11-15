from django.contrib import admin
"""from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock_quantity', 'created_at', 'updated_at', 'low_stock_alert')
    search_fields = ('name',)

    def low_stock_alert(self, obj):
        if obj.stock_quantity < 10:  # Example threshold for low stock
            return "Low Stock"
        return "Sufficient"
    low_stock_alert.short_description = 'Low Stock Alert'
    low_stock_alert.admin_order_field = 'stock_quantity'  # This allows sorting by stock quantity

admin.site.register(Product, ProductAdmin)
"""