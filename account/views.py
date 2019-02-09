from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.permissions import IsAuthenticated

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

    lookup_url_kwarg = 'pk'
    #permission_classes = (IsAuthenticated,)
    #def get_queryset(self):
        #print("hellooo", self.request.user.user_prof)
        #return [self.request.user.user_prof]
    queryset = User.objects.all()
    #queryset = User.objects.filter(pk=pk)
    serializer_class = UserDetailsSerializer
