from rest_framework import serializers
from .models import Product, Category, Review

'''class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']'''

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='get_category_display', read_only=True)
    subcategory_name = serializers.CharField(source='get_subcategory_display', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock_quantity', 'image', 'category', 'subcategory', 'category_name', 'subcategory_name', 'seller']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'buyer']
        read_only_fields = ['buyer']
