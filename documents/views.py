from astroid.protocols import objects
from django.http import JsonResponse
from django.db.models import Q, aggregates
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import api_view
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from taggit.models import Tag

from account.models import Committee, Member, Role, User

from .models import Document, Permission
from .serializers import (DocumentSerializer, FullDocumentDetailsSerializer,
                          PermissionSerializer, PermissionSerializerBasic)

# class ListDocuments(ListAPIView):
# """View to list all present documents and create new ones.

# GET:
# [
# {
# "id": 1,
# "name": "New doco",
# "description": "",
# "added_on": "2019-01-15T10:26:57.826864Z",
# "owner": null
# },
# {
# "id": 2,
# "name": "New doc2",
# "description": "66666666666666",
# "added_on": "2019-01-29T08:44:10.254867Z",
# "owner": 1
# },
# {
# "id": 3,
# "name": "llllll",
# "description": "66666666666666",
# "added_on": "2019-01-29T08:50:05.612591Z",
# "owner": 1
# },
# {
# "id": 4,
# "name": "llllll",
# "description": "66666666666666",
# "added_on": "2019-01-29T09:08:27.920592Z",
# "owner": 1
# }
# ]

# """

# queryset = Document.objects.all()

# serializer_class = DocumentSerializer


@api_view(['GET'])
def ListDocuments(request):
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
    description": "66666666666666",
    "added_on": "2019-01-29T09:08:27.920592Z",
    "owner": 1
    }
    ]

    """
    # TODO: Find  a better way to do this. 
    ### What can be done to simplify 'viewable'?
    user = request.user.user_prof
    docs = Document.objects.all()
    l = []
    for doc in docs:
        l.append({
            "id": doc.id,
            "name": doc.name,
            "added_on": doc.added_on,
            "owner": doc.owner.id if doc.owner else doc.owner,
            "description": doc.description,
            "viewable": doc.viewable_by(user),
            "shareable": doc.shareable_by(user)
        })
    return JsonResponse(l, status=200, safe=False)


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

    def perform_create(self, serializer):
        typ = self.request.data['type'].strip()
        print(self.request.data)
        pk = int(self.request.data['id'])
        document = int(self.request.data['document'])
        document = Document.objects.get(pk=document)
        level = self.request.data['level']

        u = self.request.user.user_prof
        if not document.shareable_by(u):
            print("Thou shalt not share.")
            return Response(status=status.HTTP_403_FORBIDDEN)

        elif typ == 'role':
            obj = get_object_or_404(Role, pk=pk)
            p = Permission.objects.create(
                document=document, holder=obj, level=level)
            return Response(PermissionSerializer(p).data)
        elif typ == 'committee':
            obj = get_object_or_404(Committee, pk=pk)
            p = Permission.objects.create(
                document=document, holder=obj, level=level)
            return Response(PermissionSerializer(p).data)
        elif typ == 'user':
            obj = get_object_or_404(User, pk=pk)
            p = Permission.objects.create(
                document=document, holder=obj, level=level)
            return Response(PermissionSerializer(p).data)
        else:
            print("wrong type.")
            print(typ)
            print(typ == 'role')
            return Response("No such type found.", status=status.HTTP_404_NOT_FOUND)

    serializer_class = PermissionSerializerBasic


# class DocumentDetails(RetrieveAPIView):
    # """Details of the doc if user has sufficient perms.

    # GET:
        # {
            # "id": 4,
            # "file": "http://127.0.0.1:8000/media/documents/2019/01/29/dvQce79wim7zY7YcRRPrVLr557Ug43.pdf",
            # "name": "llllll",
            # "description": "66666666666666",
            # "added_on": "2019-01-29T09:08:27.920592Z",
            # "owner": 1
        # }
# """

    # lookup_url_kwarg = 'pk'

    # def get_queryset(self):
        # user = self.request.user.user_prof
        # query = (Q(permission__user_permits=user) | Q(
            # permission__comm_permits__com_roles__member__user=user) | Q(permission__role_permits__member__user=user))
        # perms = Document.objects.filter(query)

        # return perms

    # serializer_class = FullDocumentDetailsSerializer

@api_view(['GET'])
def document_details(request, pk):
    """Details of the doc if the user has sufficient perms."""

    user = request.user.user_prof
    doc = get_object_or_404(Document, pk=pk)
    if doc.viewable_by(user):
        l = {
            "id": doc.id,
            "name": doc.name,
            "added_on": doc.added_on,
            "owner": doc.owner.id if doc.owner else doc.owner,
            "description": doc.description,
            "viewable": doc.viewable_by(user),
            "shareable": doc.shareable_by(user),
            "owner": doc.owner.user.username,
            "file": request.META['HTTP_HOST']+doc.file.url
            }
        return JsonResponse(l, status=200, safe=False)
    else:
        return Response(status=403)


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

    def perform_create(self, serializer):
        d = serializer.save(owner=self.request.user.user_prof)
        Permission.objects.create(
            document=d, holder=self.request.user.user_prof, level=1)


class SearchDocuments(ListAPIView):
    """ Document Search view with filter and ordering. Need to add other field like users, committees e.t.c in search result"""

    serializer_class = DocumentSerializer
    queryset = Document.objects.all()
    filter_backends = (filters.SearchFilter,
                       DjangoFilterBackend, filters.OrderingFilter,)
    search_fields = ('name', 'description', 'tags__name', 'added_on', )
    filter_fields = ('name', 'description', 'tags__name', 'added_on', 'owner')
    ordering_fields = ('added_on',)
