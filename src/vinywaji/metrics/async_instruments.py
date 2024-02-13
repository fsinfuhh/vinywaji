from functools import reduce
from operator import add
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
        unit="count",
    )
    vinywaji_meter.create_observable_gauge(
        "vinywaji_balances",
        callbacks=[calc_asset_aggregates],
        description="The aggregated value of account balances recorded in vinywaji (in euro-cent) ",
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
    balances = [
        i["current_balance"]
        for i in models.User.objects.all().annotate(current_balance=Sum("transactions__amount")).values()
    ]

    yield Observation(attributes={"balances": "all", "aggregate_type": "sum"}, value=reduce(add, balances, 0))
    yield Observation(
        attributes={"balances": "all", "aggregate_type": "avg"},
        value=reduce(add, balances, 0) / len(balances),
    )
    yield Observation(
        attributes={"balances": "negative", "aggregate_type": "sum"},
        value=reduce(add, (i for i in balances if i < 0), 0),
    )
    yield Observation(
        attributes={"balances": "negative", "aggregate_type": "avg"},
        value=reduce(add, (i for i in balances if i < 0), 0) / len(balances),
    )
    yield Observation(
        attributes={"balances": "positive", "aggregate_type": "sum"},
        value=reduce(add, (i for i in balances if i > 0), 0),
    )
    yield Observation(
        attributes={"balances": "positive", "aggregate_type": "avg"},
        value=reduce(add, (i for i in balances if i > 0), 0) / len(balances),
    )
