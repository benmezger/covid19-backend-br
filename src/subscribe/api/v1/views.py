from rest_framework import generics, serializers, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.throttling import UserRateThrottle

from subscribe.models import Subscribe


class SubscribeView(viewsets.ViewSet, generics.CreateAPIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Subscribe
            fields = ("email",)

    permission_classes = (AllowAny,)
    serializer_class = InputSerializer
    throttle_classes = (UserRateThrottle,)
