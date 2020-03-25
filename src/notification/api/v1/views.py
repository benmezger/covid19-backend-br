from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from notification.models import Notification
from notification import services
from notification.api.v1.serializers import (
    NotificationInputSerializer,
    NotificationOutputSerializer,
)


class NotificationViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet,
):
    queryset = Notification.objects.all()
    serializer_class = NotificationOutputSerializer
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        serializer_map = {
            "create": NotificationInputSerializer,
        }
        return serializer_map.get(self.action, super().get_serializer_class())

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        notification = services.notification_create(**serializer.validated_data)

        return Response(
            NotificationOutputSerializer(instance=notification).data,
            status=status.HTTP_201_CREATED,
        )
