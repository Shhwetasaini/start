from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import UserManager

class CustomUser(AbstractUser):
    ROLE_CHOICES = (("admin", "Admin"), ("seller", "Seller"), ("buyer", "Buyer"))

    email = models.EmailField(unique=True)
    seller = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="buyer")
    address = models.TextField(blank=True, null=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "role"]

    def __str__(self):
        return self.email
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )