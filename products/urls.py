from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/reviews/', views.ReviewCreateView.as_view(), name='product-review-create'),
    path('products/<int:product_id>/reviews/', views.ReviewCreateView.as_view(), name='product-reviews-list'),
]
