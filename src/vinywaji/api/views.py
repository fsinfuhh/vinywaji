from django.conf import settings
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from vinywaji.core import models

from . import permissions, serializers


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        if self.action == "list":
            return [IsAdminUser()]
        elif self.action == "me":
            return [IsAuthenticated()]
        else:
            return [(IsAdminUser | permissions.IsSelf)()]

    @action(detail=False)
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


@extend_schema_view(
    create=extend_schema(
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
                description="Type of transaction. If not given, negative transactions count as purchases and positive ones as deposits.",
            ),
        ]
    )
)
class TransactionViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.TransactionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return models.Transaction.objects.all()
        else:
            return models.Transaction.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action == "list":
            return [IsAuthenticated()]
        else:
            return [(IsAdminUser | permissions.IsRelatedToRequester)()]
