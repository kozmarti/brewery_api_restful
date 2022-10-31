from urllib import request
from beermanagment import services
from beermanagment.models import Reference, Bar, Stock, Order
from beermanagment.serializers import ReferenceSerializer, BarSerializer, StockSerializer, OrderSerializer
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from . import permissions


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'beers': reverse('reference-list', request=request, format=format),
        'bars': reverse('bar-list', request=request, format=format),
        'stocks': reverse('stock-list', request=request, format=format),
        'statistics': reverse('statistics', request=request, format=format),
        'orders': reverse('order-list', request=request, format=format)
    })


class ReferenceViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [permissions.IsStaffOrReadOnly]
    search_fields = ['reference', 'name', 'description']
    ordering_fields = ['reference', 'name', 'stock']


class BarViewSet(viewsets.ModelViewSet):
    queryset = Bar.objects.all()
    serializer_class = BarSerializer
    permission_classes = [permissions.IsStaffOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsStaffAndReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reference', 'bar']


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsStaffAndReadOnly | permissions.IsNotStaffReadAndWrite ]


@api_view(['GET'])
@permission_classes([permissions.IsStaffAndReadOnly])
def statistics(request):
    bars = services.get_full_and_non_full_bars()
    return Response({"all_stocks" : {
        "description": "Liste des comptoirs qui ont toutes les références en stock",
        "bars": bars['all_stocks']
    },
    "miss_at_least_one": {
        "description": "Liste des comptoirs qui ont au moins une référence épuisée",
        "bars":  bars['miss_at_least_one']
    }
    })