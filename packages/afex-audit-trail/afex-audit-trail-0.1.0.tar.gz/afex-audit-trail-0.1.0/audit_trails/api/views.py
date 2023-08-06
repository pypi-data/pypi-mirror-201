from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework.views import APIView

from audit_trails.api.serializers import NotificationListSerializer
from audit_trails.models import Notification


# Create your views here.


class MarkAsReadAPIView(APIView):

    def post(self, request, *args, **kwargs):

        try:
            notification = request.user.notifications.get(
                id=kwargs.get('notification_id')
            )
            notification.is_read = True
            notification.save()
            return Response({
                'responseCode': 100,
                'message': "Data modified successfully"
            })

        except Notification.DoesNotExist:
            return Response({
                'responseCode': 103,
                'errors': "No such notification exists",
                'message': "An error occurred"
            })


class MarkAsUnReadAPIView(APIView):

    def post(self, request, *args, **kwargs):

        try:
            notification = request.user.notifications.get(
                id=kwargs.get('notification_id')
            )
            notification.is_read = False
            notification.save()
            return Response({
                'responseCode': 100,
                'message': "Data modified successfully"
            })

        except Notification.DoesNotExist:
            return Response({
                'responseCode': 103,
                'error': "No such notification exists",
                'message': "An error occurred"
            })


class AllNotificationListAPIView(APIView):
    # authentication_classes = (JWTAuthentication,)

    def get(self, request, *args, **kwargs):
        queryset = request.user.notifications.all()
        serializer = NotificationListSerializer(
            queryset, many=True, context={'request': request}
        )

        return Response({
            'responseCode': 100,
            'data': serializer.data,
            'message': "Notification list retrieved successfully"
        })


class UnreadNotificationListAPIView(APIView):

    def get(self, request, *args, **kwargs):
        queryset = request.user.notifications.unread()
        serializer = serialize('json', queryset)

        return Response({
            'responseCode': 100,
            'data': serializer,
            'message': "Data retrieved successfully"
        })


class MarkAllNotificationsReadAPIView(APIView):

    def post(self, request, *args, **kwargs):
        request.user.notifications.mark_all_as_read()

        return Response({
            'responseCode': 100,
            'message': "Data modified successfully"
        })


class MarkAllNotificationsUnreadAPIView(APIView):

    def post(self, request, *args, **kwargs):
        request.user.notifications.mark_all_as_unread()

        return Response({
            'responseCode': 100,
            'message': "Data modified successfully"
        })

