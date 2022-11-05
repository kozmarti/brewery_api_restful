from django.test import TestCase
from beermanagment import services
from beermanagment.models import Bar, Reference, Stock
from rest_framework import serializers


class TestServiceMethods(TestCase):
    fixtures = ["fixtures.json"]

    def test_service_get_full_and_non_full_bars(self):
        bars = services.get_full_and_non_full_bars(Bar.objects.all(), Reference.objects.all().values_list('id', flat=True))
        self.assertEqual(bars['all_stocks'], [1, 3, 4])
        self.assertEqual(bars['miss_at_least_one'], [2])

    def test_is_reference_on_stock(self):
        stock = Stock.objects.get(bar=1, reference=1)
        stock.stock = 20
        order_valid = {
            "bar": 1,
            "items": [
                {
                    "reference": 1,
                    "count": 2
                }
            ]
        }
        self.assertEqual(services.is_reference_on_stock(order_valid), None)
        order_invalid = {
            "bar": 1,
            "items": [
                {
                    "reference": 1,
                    "count": 20
                }
            ]
        }
        with self.assertRaises(serializers.ValidationError):
            services.is_reference_on_stock(order_invalid)

    def test_decrease_stock(self):
        stock = Stock.objects.get(bar=1, reference=1)
        stock.stock = 20
        stock.save()
        order_valid = {
            "bar": 1,
            "items": [
                {
                    "reference": 1,
                    "count": 2
                }
            ]
        }
        services.decrease_stock(order_valid)
        self.assertEqual(18, Stock.objects.get(bar=1, reference=1).stock)
