from rest_framework.serializers import ModelSerializer, Serializer

from .models import Approval, Node, Process


class NodeSerializer(ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'


class ProcessSerializer(ModelSerializer):
    node = NodeSerializer(many=True)
    class Meta:
        model = Process
        fields = '__all__'
