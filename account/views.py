from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import (ListCreateAPIView, RetrieveAPIView,
                                     RetrieveUpdateAPIView, ListAPIView)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Committee, Member, Role, User
from .serializers import *


class ListCreateCommittees(ListCreateAPIView):
    """View to list all committess, or add more.

    Administrators may add committees using the POST method.

    GET:
        [
            {
                "id": 1,
                "com_roles": [
                    {
                        "username": "dowoop",
                        "role": "Member"
                    },
                    {
                        "username": "dowoop",
                        "role": "Member22"
                    }
                ],
                "name": "New Comm",
                "created": "2019-01-14T13:36:23.552173Z",
                "description": "New Comm 1",
                "owner": 1
            }
        ]

    POST:
        {
            "name": "",
            "description": "",
            "owner": user-id-of-user
        }

    """

    permission_classes = (IsAuthenticated,)
    queryset = Committee.objects.all()
    serializer_class = CommitteeSerializer


class CommitteeDetails(RetrieveAPIView):
    """Show details of a particular committee.

    GET:
            {
                "id": 1,
                "com_roles": [
                    {
                        "username": "dowoop",
                        "role": "Member"
                    },
                    {
                        "username": "dowoop",
                        "role": "Member22"
                    }
                ],
                "name": "New Comm",
                "created": "2019-01-14T13:36:23.552173Z",
                "description": "New Comm 1",
                "owner": 1
            }
    """

    queryset = Committee.objects.all()
    serializer_class = CommitteeSerializer
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = 'pk'





class AdditionalTokenObtainPairView(TokenObtainPairView):
    """View to get user token.

    Also returns user_id and username along with token.

    POST:
        {
            "username": "",
            "password": ""
        }
    OUT:
        {
            "refresh": "",
            "access": ""
        }
    """
    serializer_class = AdditionalTokenObtainPairSerializer


class ProfileDetailsView(RetrieveUpdateAPIView):
    """View to get user details or update them."""

    lookup_url_kwarg = 'username'
    lookup_field = 'username'
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer


class RolesView(ListCreateAPIView):
    """DEPRECATED: View to list and create roles for a certain committee."""
    # TODO: Add object level permission allowing write access to owners only.

    def get_queryset(self):
        return Role.objects.filter(committee__pk=self.kwargs['pk'])

    permission_classes = (IsAdminUser,)
    serializer_class = RoleSerializer
    #permission_classes = (IsAuthenticated,)


@api_view(http_method_names=['POST'])
def add_member(request, pk):
    """
    Add member to committee, by the owner.

    POST:
        {
        "username": "xxxx",
        "role": "yyyy"
        }
    """
    u = request.data['username']
    r = request.data['role']
    comm = get_object_or_404(Committee, pk=pk)
    if comm.owner == request.user.user_prof:
        user = User.objects.get(username=u)
        role, created = Role.objects.get_or_create(committee=comm, name=r, description=".")
        m, created = Member.objects.get_or_create(role=role, user=user)
        return Response(CommitteeSerializer(comm).data, status=status.HTTP_200_OK)
    return Response("Committee can only be modified by the owner.", status=status.HTTP_403_FORBIDDEN)


class UserListView(ListAPIView):
    """
    Gets a list of all usernames available.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class RoleListView(ListAPIView):
    """Gets a list of all the roles and committees."""

    queryset = Role.objects.all()
    serializer_class = RoleCommSerializer
