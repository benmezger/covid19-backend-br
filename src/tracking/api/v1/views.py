from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from tracking import selectors, services
from notification.api.v1.serializers import NotificationOutputSerializer
from tracking.api.v1.serializers import (
    EncounterInputSerializer,
    InfectedPersonsInputSerializer,
    InfectedPersonsOutputSerializer,
    PersonInputSerializer,
    PersonOutputSerializer,
    PersonCreationOutputSerializer,
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
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=EncounterInputSerializer(many=True))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        person = request.user
        services.encounter_bulk_create(
            person_one_beacon_id=person.beacon_id,
            encounters_data=serializer.validated_data,
        )

        return Response(status=status.HTTP_201_CREATED)


class PersonViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonInputSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "beacon_id"

    _PERMISSION_CLASSES = {
        "create": (AllowAny(),),
        "update_status": (IsAuthenticated(), IsAdminUser()),
        "symptoms_report": (IsAuthenticated(),),
        "notification": (IsAuthenticated(),),
    }

    def get_serializer_class(self):
        serializer_map = {
            "symptoms_report": PersonSymptomnsReportInputSerializer,
        }
        return serializer_map.get(self.action, super().get_serializer_class())

    def get_permissions(self):
        return self._PERMISSION_CLASSES.get(self.action, super().get_permissions())

    @swagger_auto_schema(responses={200: PersonCreationOutputSerializer})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        person = services.person_create(**serializer.validated_data)

        return Response(
            PersonCreationOutputSerializer(instance=person).data,
            status=status.HTTP_201_CREATED,
        )

    @action(("POST",), detail=True)
    def update_status(self, request, pk=None, *args, **kwargs):
        """
        An update on a person user is made by a doctor
        """
        person = self.get_object()

        serializer = self.get_serializer(person, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        person = services.person_update_status(
            person=person, health_professional=request.user, status=data["status"],
        )

        return Response(
            PersonOutputSerializer(instance=person).data, status=status.HTTP_200_OK
        )

    @action(("POST",), detail=False)
    def symptoms_report(self, request, *args, **kwargs):
        serializer = PersonSymptomnsReportInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        person = request.user
        services.person_symptom_report_bulk_create(
            person=person, symptoms_ids=serializer.validated_data["symptoms_ids"]
        )

        return Response(status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: NotificationOutputSerializer})
    @action(("GET",), detail=False)
    def notification(self, request, *args, **kwargs):
        person = request.user
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
