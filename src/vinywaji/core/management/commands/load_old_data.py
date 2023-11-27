import json
import logging
from argparse import ArgumentParser

from django.core.management import BaseCommand
from django.utils import timezone
from simple_openid_connect.integrations.django import models as openid_models

from vinywaji.core import models

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load data that was dumped with dumpdata before the user model was changed"

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument("fixture", help="the path to the dumped database fixture")

    def handle(self, *args, **options):
        logging.getLogger("").setLevel(30 - options["verbosity"] * 10)
        logger.info("loading database fixture %s", options["fixture"])
        with open(options["fixture"], "r", encoding="UTF-8") as f:
            fixture_json = json.load(f)

        # re-add users
        for user_data in (
            i for i in fixture_json if i["model"] == "django_auth_mafiasi.mafiasiauthmodeluser"
        ):
            logger.info(
                "adding user %s with openid sub %s",
                user_data["fields"]["username"],
                user_data["pk"],
            )
            user, _ = models.User.objects.get_or_create(
                username=user_data["fields"]["username"],
            )
            _openid_user = openid_models.OpenidUser.objects.get_or_create(
                user=user,
                sub=user_data["pk"],
            )

        # re-add transactions
        for transact_data in (i for i in fixture_json if i["model"] == "vinywaji_core.transaction"):
            user = openid_models.OpenidUser.objects.get(sub=transact_data["fields"]["user"]).user
            parsed_datetime = timezone.datetime.strptime(
                transact_data["fields"]["time"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            aware_datetime = timezone.make_aware(parsed_datetime)

            logger.info(
                "adding transaction from %s for %s",
                aware_datetime,
                user.username,
            )

            transaction, _ = models.Transaction.objects.get_or_create(
                user=user,
                time=aware_datetime,
                defaults={
                    "description": transact_data["fields"]["description"],
                    "amount": transact_data["fields"]["amount"],
                },
            )
            transaction.time = aware_datetime
            transaction.save()
