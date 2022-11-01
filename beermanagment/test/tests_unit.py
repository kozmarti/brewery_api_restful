from django.test import TestCase
from beermanagment import services
from beermanagment.models import Bar, Order, OrderItem, Reference, Stock


class TestServiceMethods(TestCase):
    fixtures = ["fixtures.json"]

    def test_service_get_full_and_non_full_bars(self):
        bars = services.get_full_and_non_full_bars(Bar.objects.all(), Reference.objects.all().values_list('id', flat=True))
        self.assertEqual(bars['all_stocks'], [])
        self.assertEqual(bars['miss_at_least_one'], [1, 2, 3, 4])

    def test_order_change_stock(self):
        order = Order.objects.create(bar=Bar.objects.get(pk=1))
        OrderItem.objects.create(order=order, reference=Reference.objects.get(pk=1), count=1)
        OrderItem.objects.create(order=order, reference=Reference.objects.get(pk=2), count=1)
        message = ['Order (beer id: 1) OK ', 'Order (beer id: 2) OK ']
        self.assertEqual(services.order_change_stock(order), message)
        self.assertEqual(Stock.objects.get(bar=Bar.objects.get(pk=1), reference=Reference.objects.get(pk=1)).stock, 9)
        self.assertEqual(Stock.objects.get(bar=Bar.objects.get(pk=1), reference=Reference.objects.get(pk=2)).stock, 7)

        order = Order.objects.create(bar=Bar.objects.get(pk=1))
        OrderItem.objects.create(order=order, reference=Reference.objects.get(pk=1), count=30)
        OrderItem.objects.create(order=order, reference=Reference.objects.get(pk=2), count=30)
        message = ['Only 9 beer was in stock for beer (id: 1), 21 could not be sold to customer! ',
                   'Stock for beer (id: 1) is less than 2, refill needed! ',
                   'Only 7 beer was in stock for beer (id: 2), 23 could not be sold to customer! ',
                   'Stock for beer (id: 2) is less than 2, refill needed! ']
        self.assertEqual(services.order_change_stock(order), message)
        self.assertEqual(Stock.objects.get(bar=Bar.objects.get(pk=1), reference=Reference.objects.get(pk=1)).stock, 0)
        self.assertEqual(Stock.objects.get(bar=Bar.objects.get(pk=1), reference=Reference.objects.get(pk=2)).stock, 0)

        order = Order.objects.create(bar=Bar.objects.get(pk=1))
        OrderItem.objects.create(order=order, reference=Reference.objects.get(pk=1), count=30)
        OrderItem.objects.create(order=order, reference=Reference.objects.get(pk=2), count=30)
        message = ['There is no beer (id: 1) on stock in this bar! ',
                   'There is no beer (id: 2) on stock in this bar! ']
        self.assertEqual(services.order_change_stock(order), message)
        self.assertEqual(Stock.objects.get(bar=Bar.objects.get(pk=1), reference=Reference.objects.get(pk=1)).stock, 0)
        self.assertEqual(Stock.objects.get(bar=Bar.objects.get(pk=1), reference=Reference.objects.get(pk=2)).stock, 0)

        order = Order.objects.create(bar=Bar.objects.get(pk=4))
        OrderItem.objects.create(order=order, reference=Reference.objects.get(pk=1), count=30)
        OrderItem.objects.create(order=order, reference=Reference.objects.get(pk=2), count=30)
        message = 'There is no beer at all on stock in this empty bar! '
        self.assertEqual(services.order_change_stock(order), message)

