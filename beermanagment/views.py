from django.shortcuts import render
from beermanagment.models import Reference
from beermanagment.serializers import ReferenceSerializer
from rest_framework import generics


class ReferenceList(generics.ListCreateAPIView):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer


class ReferenceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer