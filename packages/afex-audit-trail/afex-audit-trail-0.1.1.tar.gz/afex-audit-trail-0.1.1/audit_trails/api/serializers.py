from rest_framework import serializers

from audit_trails.models import Notification


class NotificationListSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = (
            'id',
            'level',
            'description',
            'timestamp',
            'timesince',
            'is_read'
        )

    def get_description(self, obj):
         request_user = self.context.get('request').user
         if obj.actor == request_user:
             return f"You {obj.action} {str(obj.action_object)}"
         return f"{obj.actor} {obj.action} {str(obj.action_object)}"
