from django.shortcuts import render
from rest_framework import viewsets

from records.models import Record
from records.serializers import RecordSerializer


# Create your views here.
class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    