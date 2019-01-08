from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import User, Member, Role, Committee

from .models import Document, Permission
from .serializers import DocumentSerializer


class ListDocuments(ListCreateAPIView):
    """View to list all present documents and create new ones."""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


@api_view()
def ViewableDocuments(request):
    """View to list the documents view-able by the user."""

    user = (User.objects.get(username='user11'))
    print(user)
    print('--------------------------')
    #user_perms = Permission.objects.filter(holder=user)
    print(user.permit_obj.all())
    return Response(user.permit_obj.all())
