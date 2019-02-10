from astroid.protocols import objects
from django.db.models import Q, aggregates
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import api_view
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from taggit.models import Tag

from account.models import Committee, Member, Role, User

from .models import Document, Permission
from .serializers import (DocumentSerializer, FullDocumentDetailsSerializer,
                          PermissionSerializer)


class ListDocuments(ListAPIView):
    """View to list all present documents and create new ones.

    GET:
        [
            {
                "id": 1,
                "name": "New doco",
                "description": "",
                "added_on": "2019-01-15T10:26:57.826864Z",
                "owner": null
            },
            {
                "id": 2,
                "name": "New doc2",
                "description": "66666666666666",
                "added_on": "2019-01-29T08:44:10.254867Z",
                "owner": 1
            },
            {
                "id": 3,
                "name": "llllll",
                "description": "66666666666666",
                "added_on": "2019-01-29T08:50:05.612591Z",
                "owner": 1
            },
            {
                "id": 4,
                "name": "llllll",
                "description": "66666666666666",
                "added_on": "2019-01-29T09:08:27.920592Z",
                "owner": 1
            }
        ]

    """

    queryset = Document.objects.all()

    serializer_class = DocumentSerializer


class ViewableDocuments(ListCreateAPIView):
    """View to list the documents view-able by the user.

    GET:
    [
        {
            "document": {
                "id": 1,
                "file": "http://127.0.0.1:8000/media/documents/2019/01/15/MPPHV4Iq0em9athVMmexdLIHlmAFRN",
                "name": "New doc yo",
                "description": "",
                "added_on": "2019-01-15T10:26:57.826864Z",
                "owner": null
            },
            "id": 1,
            "level": 0
        },
        {
            "document": {
                "id": 4,
                "file": "http://127.0.0.1:8000/media/documents/2019/01/29/dvQce79wim7zY7YcRRPrVLr557Ug43.pdf",
                "name": "llllll",
                "description": "66666666666666",
                "added_on": "2019-01-29T09:08:27.920592Z",
                "owner": 1
            },
            "id": 4,
            "level": 1
        }
    ]
    """

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        print(self.request.user)
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
    """Details of the doc if user has sufficient perms.

    GET:
        {
            "id": 4,
            "file": "http://127.0.0.1:8000/media/documents/2019/01/29/dvQce79wim7zY7YcRRPrVLr557Ug43.pdf",
            "name": "llllll",
            "description": "66666666666666",
            "added_on": "2019-01-29T09:08:27.920592Z",
            "owner": 1
        }
"""

    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        user = self.request.user.user_prof
        query = (Q(permission__user_permits=user) | Q(
            permission__comm_permits__com_roles__member__user=user) | Q(permission__role_permits__member__user=user))
        perms = Document.objects.filter(query)

        return perms

    serializer_class = FullDocumentDetailsSerializer


class DocumentCreate(CreateAPIView):
    """Add new documents and assign share perms to the user.

    POST:
        {
            "file": null,
            "name": "",
            "description": ""
        }
"""

    serializer_class = FullDocumentDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        print(request.data, args, kwargs)
        obj = Document.objects.create(
            name=request.data['name'],
            file=request.data['file'],
            owner=request.user.user_prof,
            description=request.data['description'] if 'description' in request.data.keys() else ''
        )
        print(obj, obj.owner)
        perm = Permission.objects.create(document=obj, level=1, holder=request.user.user_prof)
        print(perm)
        return Response(FullDocumentDetailsSerializer(obj).data)


class SearchDocuments(ListAPIView):
    """ Document Search view with filter and ordering. Need to add other field like users, committees e.t.c in search result"""

    serializer_class = DocumentSerializer
    queryset = Document.objects.all()
    filter_backends = (filters.SearchFilter,
                       DjangoFilterBackend, filters.OrderingFilter,)
    search_fields = ('name', 'description', 'tags__name', 'added_on', )
    filter_fields = ('name', 'description', 'tags__name', 'added_on', 'owner')
    ordering_fields = ('added_on',)
