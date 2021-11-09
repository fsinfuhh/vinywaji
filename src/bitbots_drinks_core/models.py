import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


def uuid_default() -> "uuid.UUID":
    return uuid.uuid4()


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid_default)

    REQUIRED_FIELDS = []

    def get_or_create_auth_token(self) -> Token:
        token, _ = Token.objects.get_or_create(user=self)
        return token

    @property
    def current_balance(self) -> int:
        return sum((t.amount for t in self.transactions.all()))


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_default)
    user = models.ForeignKey(to="User", on_delete=models.CASCADE, related_name="transactions", editable=False)
    description = models.CharField(max_length=30, default="")
    amount = models.IntegerField()

    def __str__(self):
        if self.description != "":
            return f"{self.user.get_username()}: {self.description}"
        else:
            verb = "spent" if self.amount < 0 else "gained"
            return f"{self.user.get_username()} {verb} {abs(self.amount)}€"
