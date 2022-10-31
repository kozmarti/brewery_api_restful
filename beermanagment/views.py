from beermanagment.models import Reference, Bar, Stock, Order
from beermanagment.serializers import ReferenceSerializer, BarSerializer, StockSerializer, OrderSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['reference', 'name', 'description']
    ordering_fields = ['reference', 'name', 'stock']


class BarViewSet(viewsets.ModelViewSet):
    queryset = Bar.objects.all()
    serializer_class = BarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reference', 'bar']


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def statistics(request):
    # service to get list of full and non full bars here
    return Response({"all_stocks" : {
        "description": "Liste des comptoirs qui ont toutes les références en stock",
        "bars": [1]
    },
    "miss_at_least_one": {
        "description": "Liste des comptoirs qui ont au moins une référence épuisée",
        "bars": [2, 3 , 4]
    }
    })