from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_migrate
from django.dispatch import receiver

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    ELECTRONICS = 1
    CLOTHING = 2
    CATEGORY_CHOICES = (
        (ELECTRONICS, "Electronics"),
        (CLOTHING, "Clothing"),
    )

    MOBILE_PHONES = 1
    SMARTPHONES = 2
    LAPTOPS = 3
    TVS = 4
    MENS_CLOTHING = 5
    WOMENS_CLOTHING = 6
    SUBCATEGORY_CHOICES = (
        (MOBILE_PHONES, "Mobile Phones"),
        (SMARTPHONES, "Smartphones"),
        (LAPTOPS, "Laptops"),
        (TVS, "TVs"),
        (MENS_CLOTHING, "Men's Clothing"),
        (WOMENS_CLOTHING, "Women's Clothing"),
    )

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    subcategory = models.IntegerField(choices=SUBCATEGORY_CHOICES, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_category_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, "Unknown Category")

    def get_subcategory_display(self):
        return dict(self.SUBCATEGORY_CHOICES).get(self.subcategory, "Unknown Subcategory")

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()

    def __str__(self):
        return f"{self.product.name} Rating: {self.rating}"
