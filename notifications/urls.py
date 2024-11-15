from django.urls import path
from .views import NotificationListView, MarkNotificationReadView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:notification_id>/read/', MarkNotificationReadView.as_view(), name='mark-notification-read'),
]
