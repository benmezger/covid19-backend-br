import json

from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema

from . import messages, serializers


class AuthenticationAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys):
        return ["Authentication endpoints"]


login = {
    "auto_schema": AuthenticationAutoSchema,
    "operation_summary": "Login for Staff users",
    "method": "POST",
    "request_body": serializers.LoginSerializer,
    "responses": {
        200: serializers.UserTokenSerializer,
        401: json.dumps(messages.WRONG_CREDENTIALS),
    },
}
