from typing import *

from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from django.conf import settings

from bitbots_drinks_core import models


class ServiceAccountAuthentication(BaseAuthentication):
    AUTH_SCHEME = "Service-Account"

    def authenticate_header(self, request):
        return self.AUTH_SCHEME

    def authenticate(self, request: Request) -> Optional[Tuple[Union[models.User, AnonymousUser], any]]:
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.AUTH_SCHEME.lower().encode():
            return

        if len(auth) == 1:
            raise AuthenticationFailed(
                "Invalid Service-Account Authorization header. No credentials were provided"
            )
        elif len(auth) > 2:
            raise AuthenticationFailed(
                "Invalid Service-Account Authorization header. Token should not contain spaces"
            )

        try:
            token = auth[1].decode()
        except UnicodeError:
            raise AuthenticationFailed(
                "Invalid Service-Account Authorization header. Token should be valid UTF-8"
            )

        if token != settings.SERVICE_ACCOUNT_TOKEN:
            raise AuthenticationFailed("Invalid Service-Account Authorization header. Incorrect token")

        return AnonymousUser(), type(self)
