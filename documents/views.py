from django.db.models import Q, aggregates
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Committee, Member, Role, User

from .models import Document, Permission
from .serializers import DocumentSerializer, PermissionSerializer


class ListDocuments(ListCreateAPIView):
    """View to list all present documents and create new ones."""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class ViewableDocuments(ListCreateAPIView):
    """View to list the documents view-able by the user."""

    user = (User.objects.get(username='user11'))
    print(user)
    query = Q(user_permits=user) | Q(
        comm_permits__com_roles__member__user=user
    ) | Q(
        role_permits__member__user=user
    )
    queryset = Permission.objects.filter(query)
    serializer_class = PermissionSerializer
