import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


def uuid_default() -> "uuid.UUID":
    return uuid.uuid4()


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid_default)

    REQUIRED_FIELDS = []


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_default)
    user = models.ForeignKey(to="User", on_delete=models.CASCADE, related_name="transactions")
    description = models.CharField(max_length=30, default="")
    amount = models.IntegerField()

    def __str__(self):
        if self.description != "":
            return f"{self.user.get_username()}: {self.description}"
        else:
            verb = "spent" if self.amount < 0 else "gained"
            return f"{self.user.get_username()} {verb} {abs(self.amount)}€"
