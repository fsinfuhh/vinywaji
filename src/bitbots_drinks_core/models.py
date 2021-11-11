import uuid
from django.db import models
from django_auth_mafiasi.models import MafiasiAuthModelUser
from rest_framework.authtoken.models import Token


def uuid_default() -> "uuid.UUID":
    return uuid.uuid4()


class User(MafiasiAuthModelUser):
    def get_or_create_auth_token(self) -> Token:
        token, _ = Token.objects.get_or_create(user=self)
        return token

    @property
    def current_balance(self) -> int:
        """How much money the user currently has in their account"""
        return sum((t.amount for t in self.transactions.all()))


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_default, help_text="The ID of this transaction")
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
    time = models.DateTimeField(auto_now_add=True, help_text="When this transaction occurred")

    def __str__(self):
        if self.description != "":
            return f"{self.user.get_username()}: {self.description}"
        else:
            verb = "spent" if self.amount < 0 else "gained"
            return f"{self.user.get_username()} {verb} {abs(self.amount)}€"
