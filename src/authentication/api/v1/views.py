from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from . import docs
from . import messages
from .serializers import (
    LoginSerializer,
    UserTokenSerializer,
)


@swagger_auto_schema(**docs.login)
@csrf_exempt
@api_view(("POST",))
@permission_classes((AllowAny,))
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    user = authenticate(email=data["email"], password=data["password"])

    if not user:
        return Response(messages.WRONG_CREDENTIALS, status=status.HTTP_401_UNAUTHORIZED)

    token, created = Token.objects.get_or_create(user=user)

    data = {"user": user, "access_token": token.key}
    return Response(UserTokenSerializer(data).data, status=status.HTTP_200_OK)
