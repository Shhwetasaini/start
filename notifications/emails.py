from django.core.mail import send_mail
from django.conf import settings

def send_order_confirmation(user, order):
    subject = "Order Confirmation"
    message = f"Hi {user.username}, your order {order.id} has been successfully placed."
    recipient_list = [user.email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

def send_shipping_update(user, order):
    subject = "Shipping Update"
    message = f"Hi {user.username}, your order {order.id} has been shipped."
    recipient_list = [user.email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

def send_payment_receipt(user, order):
    subject = "Payment Receipt"
    message = f"Hi {user.username}, we have received payment for your order {order.id}."
    recipient_list = [user.email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
