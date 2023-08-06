from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from audit_trails.models import Notification


# Create your views here.


class MarkAsReadView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        try:
            alert = request.user.alerts.get(
                id=kwargs.get('alert_id')
            )
            alert.is_read = True
            alert.save()
            return redirect(request.META.get('HTTP_REFERRER', '/'))

        except Notification.DoesNotExist:
            return redirect(request.META.get('HTTP_REFERRER', '/'))


class MarkAsUnReadView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        try:
            alert = request.user.alerts.get(
                id=kwargs.get('alert_id')
            )
            alert.is_read = False
            alert.save()
            return redirect(request.META.get('HTTP_REFERRER', '/'))

        except Notification.DoesNotExist:
            return redirect(request.META.get('HTTP_REFERRER', '/'))


class AllNotificationListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        notifications = request.user.notifications.all()

        return render(
            request,
            'audit_trails/list.html',
            context=notifications
        )


class UnreadNotificationListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        notifications = request.user.notifications.unread()

        return render(
            request,
            'audit_trails/list.html',
            context=notifications
        )


class MarkAllNotificationsReadView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        request.user.notifications.mark_all_as_read()

        return redirect(request.META.get('HTTP_REFERER', '/'))


class MarkAllNotificationsUnreadView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        request.user.notifications.mark_all_as_unread()

        return redirect(request.META.get('HTTP_REFERER', '/'))
