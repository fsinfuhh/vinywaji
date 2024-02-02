from typing import Iterable

from django.db.models import Avg, Sum
from opentelemetry import metrics
from opentelemetry.metrics import CallbackOptions, Observation

from vinywaji.core import models

vinywaji_meter = metrics.get_meter("vinywaji")


def create_async_instruments():
    vinywaji_meter.create_observable_counter(
        "vinywaji_transactions",
        callbacks=[count_transactions],
        description="The total number of transactions recorded in vinywaji",
    )
    vinywaji_meter.create_observable_gauge(
        "vinywaji_assets",
        callbacks=[calc_asset_aggregates],
        description="The aggregated value of assets recorded in vinywaji (in euro-cent) ",
        unit="ct",
    )


def count_transactions(_options: CallbackOptions) -> Iterable[Observation]:
    n_negative = models.Transaction.objects.filter(amount__lt=0).count()
    n_positive = models.Transaction.objects.filter(amount__gt=0).count()
    yield Observation(value=n_negative, attributes={"transaction_type": "withdrawal"})
    yield Observation(value=n_positive, attributes={"transaction_type": "deposit"})
    yield Observation(value=n_positive + n_negative, attributes={"transaction_type": "any"})


def calc_asset_aggregates(_options: CallbackOptions) -> Iterable[Observation]:
    # aggregate all negative transactions
    negative_aggregate = models.Transaction.objects.filter(amount__lt=0).aggregate(
        Sum("amount"), Avg("amount")
    )
    yield Observation(
        value=negative_aggregate["amount__sum"] or 0,
        attributes={"asset_type": "negative", "aggregate_type": "sum"},
    )
    yield Observation(
        value=negative_aggregate["amount__avg"] or 0,
        attributes={"asset_type": "negative", "aggregate_type": "avg"},
    )

    # aggregate all positive transactions
    positive_aggregate = models.Transaction.objects.filter(amount__gt=0).aggregate(
        Sum("amount"), Avg("amount")
    )
    yield Observation(
        value=positive_aggregate["amount__avg"] or 0,
        attributes={
            "asset_type": "positive",
            "aggregate_type": "sum",
        },
    )
    yield Observation(
        value=positive_aggregate["amount__sum"] or 0,
        attributes={
            "asset_type": "positive",
            "aggregate_type": "avg",
        },
    )

    # calculate totals based on previous data
    yield Observation(
        value=(positive_aggregate["amount__sum"] or 0) + (negative_aggregate["amount__sum"] or 0),
        attributes={
            "asset_type": "total",
            "aggregate_type": "sum",
        },
    )
