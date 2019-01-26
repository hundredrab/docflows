from astroid.protocols import objects
from django.db.models import Q, aggregates
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters

from account.models import Committee, Member, Role, User

from .models import Document, Permission
from .serializers import (DocumentSerializer, FullDocumentDetailsSerializer,
                          PermissionSerializer)
from taggit.models import Tag
from django_filters.rest_framework import DjangoFilterBackend
from itertools import chain


class ListDocuments(ListCreateAPIView):
    """View to list all present documents and create new ones."""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class ViewableDocuments(ListAPIView):
    """View to list the documents view-able by the user."""

    def get_queryset(self):
        print(self.request.user)
        print(User)
        user, created = User.objects.get_or_create(user=self.request.user, defaults={'username':self.request.user.username})
        #user = self.request.user.user_prof
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

class SearchDocuments(ListAPIView):
    serializer_class = DocumentSerializer
    # DocumentQueryset = Document.objects.all()
    # UserQueryset = User.objects.all()
    # CommitteeQueryset = Committee.objects.all()
    # MemberQueryset = Member.objects.all()
    # RoleQueryset = Role.objects.all()
    # queryset = DocumentQueryset.union(UserQueryset, CommitteeQueryset, MemberQueryset, RoleQueryset)
    queryset = Document.objects.all() 
    # queryset = sorted(chain(DocumentQueryset, UserQueryset, CommitteeQueryset, MemberQueryset, RoleQueryset))
    filter_backends = (filters.SearchFilter,DjangoFilterBackend,)
    search_fields = ('name', 'description', 'tags__name', 'added_on', )
    filter_fields = ('name', 'description', 'tags__name', 'added_on', )
