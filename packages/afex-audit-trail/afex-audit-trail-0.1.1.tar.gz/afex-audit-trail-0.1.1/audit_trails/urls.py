from django.urls import path

from .views import (
    AllNotificationListView, UnreadNotificationListView,
    MarkAsReadView, MarkAsUnReadView, MarkAllNotificationsReadView,
    MarkAllNotificationsUnreadView
)

app_name = 'audit_trails'

urlpatterns = [
    path('', AllNotificationListView.as_view(), name="notifications"),
    path('unread', UnreadNotificationListView.as_view(), name="unread_notifications"),
    path('<int:notification_id>/mark_as_read', MarkAsReadView.as_view(), name="mark_as_read"),
    path('<int:notification_id>/mark_as_unread', MarkAsUnReadView.as_view(), name="mark_as_unread"),
    path('mark_all_as_read', MarkAllNotificationsReadView.as_view(), name="mark_all_read"),
    path('mark_all_as_unread', MarkAllNotificationsUnreadView.as_view(), name="mark_all_unread"),
]
