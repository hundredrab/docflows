from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView

from .models import Committee, Member, Role, User
from .serializers import CommitteeSerializer


class ListCreateCommittees(ListCreateAPIView):
    """View to list or add committess.

    Administrators may add committees using the POST method."""

    queryset = Committee.objects.all()
    serializer_class = CommitteeSerializer
