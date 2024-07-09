import uuid
import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


def uuid_default() -> "uuid.UUID":
    return uuid.uuid4()


def webhook_trigger_default() -> str:
    return secrets.token_urlsafe(64)


class User(AbstractUser):
    @property
    def current_balance(self) -> int:
        """How much money the user currently has in their account"""
        aggregate = self.transactions.aggregate(
            transaction_sum=models.Sum("amount", default=0)
        )
        return aggregate["transaction_sum"]


class Transaction(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid_default, help_text="The ID of this transaction"
    )
    user = models.ForeignKey(
        to="User",
        on_delete=models.CASCADE,
        related_name="transactions",
        editable=False,
        help_text="The user with which this transaction is associated",
    )
    description = models.CharField(
        max_length=30,
        default="",
        help_text="Additional free form details a user might wish to add to this transaction",
    )
    amount = models.IntegerField(
        help_text="How much money was involved in this transaction in euro-cent. "
        "Negative amounts represent purchases while positive amounts represent deposits."
    )
    time = models.DateTimeField(
        auto_now_add=True, help_text="When this transaction occurred"
    )

    def __str__(self):
        if self.description != "":
            return f"{self.user.get_username()}: {self.description}"
        else:
            verb = "spent" if self.amount < 0 else "gained"
            return f"{self.user.get_username()} {verb} {abs(self.amount)}€"


class WebhookConfig(models.Model):
    """
    Users can create webhooks that trigger specific transactions.
    This model stores the configuration of what each webhook exactly does.
    """

    id = models.UUIDField(
        primary_key=True, default=uuid_default, help_text="The ID of this webhook"
    )
    description = models.CharField(
        max_length=128,
        help_text="A free-form description which the user can give this webhook",
        default="",
        null=False,
        blank=True,
    )
    transaction_description = models.CharField(
        max_length=30,
        help_text="The description that will be added to the transaction when this webhook is triggered",
        default="",
        null=False,
        blank=True,
    )
    trigger_key = models.CharField(
        max_length=64,
        help_text="The key required to trigger this webhook",
        default=webhook_trigger_default,
        editable=False,
    )
    user = models.ForeignKey(
        to="User",
        on_delete=models.CASCADE,
        related_name="webhooks",
        editable=False,
        help_text="The user who configured this webhook and who is impacted when it is called",
    )
    amount = models.IntegerField(
        help_text="How much money the triggered transaction records in euro-cent. Negative amounts represent purchases while positive amounts represent deposits.",
    )

    def __str__(self):
        return f"Webhook {self.id} (/{self.trigger_key})"

    def get_absolute_url(self) -> str:
        return reverse("webhook-trigger", kwargs={"pk": self.pk})

    def trigger(self) -> Transaction:
        """
        Trigger this webhook and create the configured transaction
        """
        return Transaction.objects.create(
            user=self.user,
            description=self.transaction_description,
            amount=self.amount,
        )