from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from .models import Process
from .serializers import ProcessSerializer


class ListProcesses(ListCreateAPIView):
    """View to list all present processes and create new ones."""

    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
