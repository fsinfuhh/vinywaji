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
    amount = serializers.FloatField()

    def create(self, validated_data):
        if self.context["request"].query_params.get("currency") == "euro":
            validated_data["amount"] = validated_data["amount"] * 100
        if self.context["request"].query_params.get("type") == "purchase":
            validated_data["amount"] = validated_data["amount"] * -1
        validated_data["amount"] = int(validated_data["amount"])
        return models.Transaction.objects.create(**validated_data)


class WebhookConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WebhookConfig
        fields = "__all__"

    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(), queryset=models.User.objects.all()
    )
    amount = serializers.FloatField()

    def create(self, validated_data):
        validated_data["amount"] = int(validated_data["amount"])
        return models.WebhookConfig.objects.create(**validated_data)
