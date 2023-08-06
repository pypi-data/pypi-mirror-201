from django.urls import path

from .views import (
    AllNotificationListAPIView, UnreadNotificationListAPIView,
    MarkAsReadAPIView, MarkAsUnReadAPIView, MarkAllNotificationsReadAPIView,
    MarkAllNotificationsUnreadAPIView
)

app_name = 'api_audit_trail'

urlpatterns = [
    path('', AllNotificationListAPIView.as_view(), name="notifications"),
    path('unread', UnreadNotificationListAPIView.as_view(), name="unread_notifications"),
    path('<int:notification_id>/mark_as_read', MarkAsReadAPIView.as_view(), name="mark_as_read"),
    path('<int:notification_id>/mark_as_unread', MarkAsUnReadAPIView.as_view(), name="mark_as_unread"),
    path('mark_all_as_read', MarkAllNotificationsReadAPIView.as_view(), name="mark_all_read"),
    path('mark_all_as_unread', MarkAllNotificationsUnreadAPIView.as_view(), name="mark_all_unread"),
]
