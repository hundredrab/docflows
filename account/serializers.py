from rest_framework.serializers import ModelSerializer

from .models import Committee, Member, Role, User

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)


class MemberSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Member
        fields = ('user',)


class RoleSerializer(ModelSerializer):
    member = MemberSerializer(many=True)

    class Meta:
        model = Role
        fields = '__all__'


class CommitteeSerializer(ModelSerializer):
    com_roles = RoleSerializer(many=True)

    class Meta:
        model = Committee
        fields = '__all__'
