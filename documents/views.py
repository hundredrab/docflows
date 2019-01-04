from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView

from .models import Document
from .serializers import DocumentSerializer


class ListDocuments(ListCreateAPIView):
    """View to list all present documents and create new ones."""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
