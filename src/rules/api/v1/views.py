from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rules.models import RuleCondition
from utils.drf.utils import inline_serializer


class RuleViewSet(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=True)
        name = serializers.CharField(required=True, source="rule.name")
        message = serializers.CharField(required=True, source="rule.message")
        any = serializers.BooleanField(required=True, source="rule.any")
        logical_conditions = inline_serializer(
            fields={
                "id": serializers.IntegerField(required=True),
                "attribute": serializers.CharField(required=True),
                "operator": serializers.CharField(required=True),
                "value": serializers.CharField(required=True),
            },
            many=True,
        )

    def get_queryset(self):
        return RuleCondition.objects.filter(rule__enabled=True)

    @swagger_auto_schema(responses={200: OutputSerializer(many=True)})
    def get(self, request):
        output = self.OutputSerializer(self.get_queryset(), many=True)
        return Response(output.data, status=status.HTTP_200_OK)
