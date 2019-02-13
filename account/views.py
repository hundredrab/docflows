from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
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

    permission_classes = (IsAuthenticated, IsAdminUser,)
    queryset = Committee.objects.all()
    serializer_class = CommitteeSerializer


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
    """View to list and create roles for a certain committee."""
    # TODO: Add object level permission allowing write access to owners only.

    def get_queryset(self):
        return Role.objects.filter(committee__pk=self.kwargs['pk'])

    permission_classes = (IsAdminUser,)
    serializer_class = RoleSerializer
    #permission_classes = (IsAuthenticated,)
