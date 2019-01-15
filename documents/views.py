from django.db.models import Q, aggregates
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Committee, Member, Role, User

from .models import Document, Permission
from .serializers import DocumentSerializer, PermissionSerializer, FullDocumentDetailsSerializer


class ListDocuments(ListCreateAPIView):
    """View to list all present documents and create new ones."""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class ViewableDocuments(ListAPIView):
    """View to list the documents view-able by the user."""

    def get_queryset(self):
        user = self.request.user.user_prof
        query = Q(user_permits=user) | Q(
            comm_permits__com_roles__member__user=user
        ) | Q(
            role_permits__member__user=user
        )
        return Permission.objects.filter(query)
    serializer_class = PermissionSerializer


@api_view
def document_details(request, id):
    """Details of the document w.r.t. user."""

    if request.method == 'GET':
        pass
