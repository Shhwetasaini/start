from django.urls import path
from .views import OrderListView, OrderDetailView, OrderUpdateStatusView

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    path('update_status/<int:order_id>/', OrderUpdateStatusView.as_view(), name='update_order_status'),
]
