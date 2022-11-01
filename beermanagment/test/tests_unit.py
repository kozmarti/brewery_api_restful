from django.test import TestCase
from beermanagment import services
from beermanagment.models import Bar, Order, OrderItem, Reference


class TestServiceMethods(TestCase):
    fixtures = ["fixtures.json"]

    def test_service_get_full_and_non_full_bars(self):
        bars = services.get_full_and_non_full_bars(Bar.objects.all(), Reference.objects.all().values_list('id', flat=True))
        self.assertEqual(bars['all_stocks'], [])
        self.assertEqual(bars['miss_at_least_one'], [1, 2, 3, 4])

    def test_order_change_stock(self):
        order = Order.objects.create(bar=Bar.objects.get(pk=1))
        OrderItem.objects.create(order=order, reference=Reference.objects.get(pk=1), count=30)
        OrderItem.objects.create(order=order, reference=Reference.objects.get(pk=2), count=30)
        message = ['Only 10 beer was in stock for beer (id: 1, 20 could not be sold to customer! ',
                   'Stock for beer (id: 1) is less than 2, refill needed! ',
                   'Only 8 beer was in stock for beer (id: 2, 22 could not be sold to customer! ',
                   'Stock for beer (id: 2) is less than 2, refill needed! ']
        self.assertEqual(services.order_change_stock(order), message)
        message = ['There is no beer (id: 1) on stock in this bar! ',
                   'There is no beer (id: 2) on stock in this bar! ']
        order = Order.objects.create(bar=Bar.objects.get(pk=1))
        OrderItem.objects.create(order=order, reference=Reference.objects.get(pk=1), count=30)
        OrderItem.objects.create(order=order, reference=Reference.objects.get(pk=2), count=30)
        self.assertEqual(services.order_change_stock(order), message)

