from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rules.api.v1.serializers import RuleConditionSerializer
from rules.models import RuleCondition
from utils.drf.utils import inline_serializer


class RuleViewSet(APIView):
    class OutputSerializer(serializers.Serializer):
        name = serializers.CharField(required=True, source="rule.name")
        message = serializers.CharField(required=True, source="rule.message")
        logical_conditions = inline_serializer(
            fields={
                "attribute": serializers.CharField(required=True),
                "operator": serializers.CharField(required=True),
                "value": serializers.CharField(required=True),
            },
            many=True,
        )

    def get_queryset(self):
        return RuleCondition.objects.filter(rule__enabled=True)

    def get(self, request):
        output = self.OutputSerializer(self.get_queryset(), many=True)
        return Response(output.data, status=status.HTTP_200_OK)
