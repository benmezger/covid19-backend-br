from rest_framework import serializers

from notification.models import Notification


class NotificationInputSerializer(serializers.Serializer):
    person_beacon_id = serializers.CharField()
    rule_id = serializers.CharField()
    delivered = serializers.BooleanField()
    read = serializers.BooleanField()


class NotificationOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "title", "message", "delivered", "read", "created")
