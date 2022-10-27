from rest_framework import serializers
from beermanagment.models import Reference, Bar, Stock, Order


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
        fields = ['id', 'reference', 'bar', 'stock']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'bar']