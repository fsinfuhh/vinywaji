from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiParameter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets, status
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


class TransactionViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "currency",
                str,
                enum=["ct", "euro"],
                description="Currency in which the provided transaction amount is. If euro, it will be converted to cents automatically.",
            ),
            OpenApiParameter(
                "type",
                str,
                enum=["purchase", "deposit"],
                description="Type of transaction. If not given, negative transactions count as purchases ans positive ones as deposits.",
            ),
        ]
    )
    def create(self, request: Request, *args, **kwargs):
        # perform preliminary validation to make sure that later data modification does not fail unexpectedly
        self.get_serializer(data=request.data).is_valid(raise_exception=True)

        # force QueryDict to be mutable
        data = request.data.copy()

        # adjust requested transaction object according to query parameters
        if "currency" in request.query_params and request.query_params["currency"] == "euro":
            data["amount"] *= 100
        if "type" in request.query_params and request.query_params["type"] == "purchase":
            data["amount"] *= -1

        # create the transaction object
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
