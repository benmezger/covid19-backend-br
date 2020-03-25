from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rules.api.v1.serializers import RuleConditionSerializer
from rules.models import Rule


class RuleViewSet(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        conditions = RuleConditionSerializer(many=True)

        class Meta:
            model = Rule
            fields = (
                "id",
                "name",
                "conditions",
            )

    def get_queryset(self):
        return Rule.objects.all()

    def get(self, request):
        output = self.OutputSerializer(self.get_queryset(), many=True)
        return Response(output.data, status=status.HTTP_200_OK)
