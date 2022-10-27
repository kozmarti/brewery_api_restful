from django.shortcuts import render
from beermanagment.models import Reference, Bar, Stock, Order
from beermanagment.serializers import ReferenceSerializer, BarSerializer, StockSerializer, OrderSerializer
from rest_framework import generics
from rest_framework import permissions


class ReferenceList(generics.ListCreateAPIView):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReferenceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    permission_classes = [permissions.IsAuthenticated]


class BarList(generics.ListCreateAPIView):
    queryset = Bar.objects.all()
    serializer_class = BarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BarDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bar.objects.all()
    serializer_class = BarSerializer
    permission_classes = [permissions.IsAuthenticated]


class StockList(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer