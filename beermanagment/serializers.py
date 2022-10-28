from rest_framework import serializers
from beermanagment.models import Reference, Bar, Stock, Order, OrderItem



class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ['id', 'reference', 'name', 'description', 'availability']


class BarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bar
        fields = ['id', 'name']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['reference', 'bar', 'stock']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['reference', 'count']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer()

    class Meta:
        model = Order
        fields = ['id', 'bar', 'items']

