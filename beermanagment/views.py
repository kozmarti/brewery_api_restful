from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from . import permissions as custom_permissions
from beermanagment import services
from beermanagment.models import Reference, Bar, Stock, Order
from beermanagment.serializers import ReferenceSerializer, BarSerializer, StockSerializer, OrderSerializer
from django.db.models import Count
from django.db.models import Q

@api_view(['GET'])
def api_root(request):
    return Response({
        'beers': reverse('reference-list', request=request),
        'bars': reverse('bar-list', request=request),
        'stocks': reverse('stock-list', request=request),
        'statistics': reverse('statistics', request=request),
        'orders': reverse('order-list', request=request)
    })


class ReferenceViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all().annotate(is_on_stock=Count('stock', filter=Q(stock__stock__gt=0)))
    serializer_class = ReferenceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [custom_permissions.IsStaffOrReadOnly]
    search_fields = ['reference', 'name', 'description']
    ordering_fields = ['reference', 'name', 'stock']


class BarViewSet(viewsets.ModelViewSet):
    queryset = Bar.objects.all()
    serializer_class = BarSerializer
    permission_classes = [custom_permissions.IsStaffOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [custom_permissions.IsStaffAndReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reference', 'bar']


class OrderList(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [custom_permissions.IsStaffAndReadOnly | custom_permissions.IsNotStaffWriteOnly ]

    def get_queryset(self):
        if custom_permissions.IsNotStaffWriteOnly.has_permission(self, self.request, self):
            return []
        else:
            return Order.objects.all()


@api_view(['GET'])
@permission_classes([custom_permissions.IsStaffAndReadOnly])
def statistics(request):
    bars = services.get_full_and_non_full_bars(Bar.objects.all(), Reference.objects.all().values_list('id', flat=True))
    return Response({"all_stocks": {
        "description": "Liste des comptoirs qui ont toutes les références en stock",
        "bars": bars['all_stocks']
    },
        "miss_at_least_one": {
        "description": "Liste des comptoirs qui ont au moins une référence épuisée",
        "bars":  bars['miss_at_least_one']
    }
    })
