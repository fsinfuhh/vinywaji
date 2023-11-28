from rest_framework import serializers

from vinywaji.core import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id", "transactions", "username", "current_balance"]

    transactions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = "__all__"

    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(), queryset=models.User.objects.all()
    )
    amount = serializers.DecimalField(max_digits=5, decimal_places=2)
