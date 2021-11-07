from rest_framework import serializers
from rest_framework.authtoken.models import Token
from bitbots_drinks_core import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id", "transactions", "username", "auth_token"]

    transactions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    auth_token = serializers.SerializerMethodField()

    def get_auth_token(self, instance: "models.User") -> str:
        token, _ = Token.objects.get_or_create(user=instance)
        return str(token)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = "__all__"

    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(), queryset=models.User.objects.all()
    )
