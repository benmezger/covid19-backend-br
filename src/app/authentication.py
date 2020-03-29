from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import TokenAuthentication

from authentication.models import PersonToken


class PersonTokenAuthentication(TokenAuthentication):
    keyword = "PersonToken"
    model = PersonToken

    def authenticate_credentials(self, key):
        model = self.get_model()

        try:
            token = model.objects.select_related("person").get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_("Invalid token."))

        return (token.person, token)
