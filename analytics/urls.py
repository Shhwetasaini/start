from django.urls import path
from .views import SalesAnalyticsView, UserBehaviorAnalyticsView, InventoryManagementView, GenerateCustomReportView, AnalyticsView

urlpatterns = [
    path('sales-analytics/', SalesAnalyticsView.as_view(), name='sales-analytics'),
    path('user-behavior-analytics/', UserBehaviorAnalyticsView.as_view(), name='user-behavior-analytics'),
    path('inventory-management/', InventoryManagementView.as_view(), name='inventory-management'),
    path('generate-report/', GenerateCustomReportView.as_view(), name='generate-custom-report'),
    path('dashboard-analytics/', AnalyticsView.as_view(), name='dashboard-analytics'),
]
