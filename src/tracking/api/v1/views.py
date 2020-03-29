from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from tracking import selectors, services
from notification.api.v1.serializers import NotificationOutputSerializer
from tracking.api.v1.serializers import (
    EncounterInputSerializer,
    InfectedPersonsInputSerializer,
    InfectedPersonsOutputSerializer,
    PersonInputSerializer,
    PersonOutputSerializer,
    PersonSymptomnsReportInputSerializer,
    RiskFactorSerializer,
    SymptomSerializer,
)
from tracking.models import Encounter, Person, RiskFactor, Symptom


@swagger_auto_schema(
    **{
        "operation_summary": "infected persons",
        "method": "POST",
        "request_body": InfectedPersonsInputSerializer,
        "responses": {200: InfectedPersonsOutputSerializer(many=True)},
    }
)
@api_view(("POST",))
@permission_classes((IsAuthenticated,))
def infected_persons(request):
    serializer = InfectedPersonsInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    queryset = selectors.get_possible_infected_persons_in_ids(
        persons_beacons_ids=serializer.validated_data["persons_beacons_ids"]
    )

    return Response(
        InfectedPersonsOutputSerializer(instance=queryset, many=True).data,
        status.HTTP_200_OK,
    )


class EncounterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Encounter.objects.all()
    serializer_class = EncounterInputSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(operation_summary="encounter_batch_create. Accepts a list.")
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        services.encounter_bulk_create(encounters_data=serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class PersonViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = Person.objects.all()
    serializer_class = PersonInputSerializer
    permission_classes = (IsAuthenticated,)

    _PERMISSION_CLASSES = {
        "create": (AllowAny(),),
        "partial_update": (IsAuthenticated(),),
        "symptoms_report": (AllowAny(),),
        "notification": (AllowAny(),),
    }

    def get_object_or_404(self, pk):
        try:
            return Person.objects.get(beacon_id=pk)
        except Person.DoesNotExist:
            raise Http404

    def get_serializer_class(self):
        serializer_map = {
            "symptoms_report": PersonSymptomnsReportInputSerializer,
        }
        return serializer_map.get(self.action, super().get_serializer_class())

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
        person = self.get_object_or_404(pk=pk)

        serializer = self.get_serializer(person, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        person = services.person_update_status(
            person=person, health_professional=request.user, status=data["status"],
        )

        return Response(
            PersonOutputSerializer(instance=person).data, status=status.HTTP_200_OK
        )

    @action(("POST",), detail=True)
    def symptoms_report(self, request, pk):
        person = self.get_object_or_404(pk=pk)

        serializer = PersonSymptomnsReportInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        services.person_symptom_report_bulk_create(
            person=person, symptoms_ids=serializer.validated_data["symptoms_ids"]
        )

        return Response(status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: NotificationOutputSerializer})
    @action(("GET",), detail=True)
    def notification(self, request, pk):
        person = self.get_object_or_404(pk=pk)
        notifications = person.notifications.all()

        return Response(NotificationOutputSerializer(notifications, many=True).data)


# Generic view. No need to overwrite anything
class RiskFactorViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = RiskFactor.objects.all()
    serializer_class = RiskFactorSerializer
    permission_classes = (AllowAny,)


# Generic view. No need to overwrite anything
class SymptomViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer
    permission_classes = (AllowAny,)
