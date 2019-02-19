from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Committee, Member, Role, User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'id')


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


class MinimalRoleSerializer(ModelSerializer):
    """Role serializer for creating new roles within specific commmittees."""

    class Meta:
        model = Role
        fields = ('name', 'description')


class RoleCommSerializer(ModelSerializer):

    class Meta:
        model = Role
        fields = ('id', 'name', 'committee', 'description')


class CommitteeSerializer(ModelSerializer):
    com_roles = serializers.ReadOnlyField(source='get_role_users')

    class Meta:
        model = Committee
        fields = '__all__'


class UserDetailsSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class AdditionalTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Passes additional data, viz., username, along with the standard token."""
    @classmethod
    def get_token(cls, user):
        token = super(AdditionalTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        token['profile-id'] = user.user_prof.id
        return token
