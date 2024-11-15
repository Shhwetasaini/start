from django.urls import path
from .views import AddToCartView, RemoveFromCartView, CheckoutView

urlpatterns = [
    path('add/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('checkout/', CheckoutView.as_view(), name='cart_checkout'),
]
