from rest_framework import serializers
from beermanagment.models import Reference


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ['id', 'reference', 'name', 'description']