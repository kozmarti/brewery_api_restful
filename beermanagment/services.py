from django.db.models import QuerySet
from beermanagment.models import Bar, Stock
from rest_framework import serializers


def get_full_and_non_full_bars(bars: QuerySet[Bar], references: list) -> dict:
    bars_full_non_full = {}
    bars_full_non_full['miss_at_least_one'] = list(set(Stock.objects.filter(stock=0).values_list('bar', flat=True)))
    bars_full_non_full['all_stocks'] = list(Bar.objects.all().exclude(id__in=bars_full_non_full['miss_at_least_one']).values_list('id', flat=True))
    return bars_full_non_full


def is_reference_on_stock(order):
    for item in order["items"]:
        if Stock.objects.get(bar=order["bar"], reference=item["reference"]).stock < item["count"]:
            raise serializers.ValidationError(f'There is not enough beer on stock to get this order.')


def decrease_stock(order):
    for item in order["items"]:
        stock_item = Stock.objects.get(bar=order["bar"], reference=item["reference"])
        stock_item.stock -= item["count"]
        stock_item.save()
