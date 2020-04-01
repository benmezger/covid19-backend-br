from rest_framework import serializers

from notification.models import Notification


class NotificationInputSerializer(serializers.Serializer):
    rule_id = serializers.CharField()
    delivered = serializers.BooleanField()
    read = serializers.BooleanField()


class NotificationOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "title", "message", "delivered", "read", "created")
