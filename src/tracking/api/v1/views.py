from django.http import Http404
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from tracking.models import Person
from tracking import services
from tracking.api.v1.serializers import PersonInputSerializer, PersonOutputSerializer


class PersonViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet,
):
    serializer_class = PersonInputSerializer
    permission_classes = (IsAuthenticated,)

    _PERMISSION_CLASSES = {
        "create": (AllowAny(),),
        "partial_update": (IsAuthenticated(),),
    }

    def get_permissions(self):
        return self._PERMISSION_CLASSES.get(self.action, super().get_permissions())

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        person = services.person_create(**serializer.validated_data)

        return Response(
            PersonOutputSerializer(instance=person).data, status=status.HTTP_201_CREATED
        )

    def partial_update(self, request, pk=None, *args, **kwargs):
        person = self.get_object(pk=pk)

        serializer = self.get_serializer(person, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        person = services.person_update_status(
            person=person, health_professional=request.user, status=data["status"],
        )

        return Response(
            PersonOutputSerializer(instance=person).data, status=status.HTTP_200_OK
        )

    def get_object(self, pk):
        try:
            return Person.objects.get(beacon_id=pk)
        except Person.DoesNotExist:
            raise Http404
