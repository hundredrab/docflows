from rest_framework.serializers import ModelSerializer, Serializer

from .models import Approval, Node, Process
from documents.serializers import DocumentSerializer


class ApprovalSerializer(ModelSerializer):

    class Meta:
        model = Approval
        fields = '__all__'


class NodeSerializer(ModelSerializer):

    class Meta:
        model = Node
        fields = '__all__'


class ProcessSerializer(ModelSerializer):
    node = NodeSerializer(many=True)
    # TODO: Fix Current-node attribute on create() to default to 0.

    class Meta:
        model = Process
        fields = '__all__'
