from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from bitbots_drinks_core import models
from . import serializers


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.UserSerializer

    @action(detail=False)
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer
