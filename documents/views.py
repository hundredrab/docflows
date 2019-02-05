from astroid.protocols import objects
from django.db.models import Q, aggregates
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters, status

from account.models import Committee, Member, Role, User

from .models import Document, Permission
from .serializers import (DocumentSerializer, FullDocumentDetailsSerializer,
                          PermissionSerializer)
from taggit.models import Tag
from django_filters.rest_framework import DjangoFilterBackend


class ListDocuments(ListAPIView):
    """View to list all present documents and create new ones."""

    queryset = Document.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.user_prof)
    serializer_class = DocumentSerializer


class ViewableDocuments(ListCreateAPIView):
    """View to list the documents view-able by the user."""

    def get_queryset(self):
        # print(self.request.user)
        # print(User)
        user, created = User.objects.get_or_create(user=self.request.user, defaults={
                                                   'username': self.request.user.username})
        #user = self.request.user.user_prof
        query = Q(user_permits=user) | Q(
            comm_permits__com_roles__member__user=user
        ) | Q(
            role_permits__member__user=user
        )
        return Permission.objects.filter(query)
    serializer_class = PermissionSerializer


class DocumentDetails(RetrieveAPIView):
    """Details of the doc w.r.t. user."""

    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        user = self.request.user.user_prof
        query = (Q(permission__user_permits=user) | Q(
            permission__comm_permits__com_roles__member__user=user) | Q(permission__role_permits__member__user=user))
        perms = Document.objects.filter(query)

        return perms

    serializer_class = FullDocumentDetailsSerializer


class SearchDocuments(ListAPIView):
    """ Document Search view with filter and ordering. Need to add other field like users, committees e.t.c in search result"""
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()
    filter_backends = (filters.SearchFilter,
                       DjangoFilterBackend, filters.OrderingFilter,)
    search_fields = ('name', 'description', 'tags__name', 'added_on', )
    filter_fields = ('name', 'description', 'tags__name', 'added_on', 'owner')
    ordering_fields = ('added_on',)
