from django.dispatch import Signal

from audit_trails.models import Notification


class Notify:

    def info(self, actor, recipients, **kwargs):
        Notification.objects.bulk_create([
            Notification(actor=actor, recipient=recipient, level='info', **kwargs)
            for recipient in recipients
        ])

    def success(self, actor, recipients, **kwargs):
        Notification.objects.bulk_create([
            Notification(actor=actor, recipient=recipient, level='success', **kwargs)
            for recipient in recipients
        ])

    def warning(self, actor, recipients, **kwargs):
        Notification.objects.bulk_create([
            Notification(actor=actor, recipient=recipient, level='warning', **kwargs)
            for recipient in recipients
        ])

    def error(self, actor, recipients, **kwargs):
        Notification.objects.bulk_create([
            Notification(actor=actor, recipient=recipient, level='error', **kwargs)
            for recipient in recipients
        ])


notify = Notify()
