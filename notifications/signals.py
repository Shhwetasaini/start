from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from orders.models import Order
from django.contrib.auth.models import User

@receiver(post_save, sender=Order)
def order_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            message=f"Your order {instance.id} has been placed successfully."
        )
    elif instance.status == "Shipped":
        Notification.objects.create(
            user=instance.user,
            message=f"Your order {instance.id} has been shipped."
        )
