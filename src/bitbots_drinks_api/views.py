from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import views
from rest_framework.decorators import action
from django.conf import settings

from bitbots_drinks_core import models
from . import serializers
from . import permissions
from .authentication import ServiceAccountAuthentication


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        if self.action == "list":
            return [(permissions.IsAdminUser | permissions.IsServiceAccount)()]
        elif self.action == "me":
            return [permissions.IsAuthenticated()]
        else:
            return [(permissions.IsAdminUser | permissions.IsServiceAccount | permissions.IsSelf)()]

    @action(detail=False)
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TransactionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.auth == ServiceAccountAuthentication:
            return models.Transaction.objects.all()
        else:
            return models.Transaction.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action == "list":
            return [(permissions.IsAuthenticated | permissions.IsServiceAccount)()]
        return [(permissions.IsAdminUser | permissions.IsServiceAccount | permissions.IsRelatedToRequester)()]


class AppSettingsViewSet(views.APIView):
    def get_permissions(self):
        return [(permissions.IsAdminUser | permissions.IsServiceAccount)()]

    @extend_schema(
        responses=inline_serializer(
            name="AppSettingsSerializer",
            fields={"service_account_token": serializers.serializers.CharField()},
        )
    )
    def get(self, request: Request) -> Response:
        return Response(
            {
                "service_account_token": settings.SERVICE_ACCOUNT_TOKEN,
            }
        )
