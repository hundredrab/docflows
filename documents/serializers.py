from rest_framework import serializers

from .models import Document, Permission


class DocumentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=True)

    class Meta:
        model = Document
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = '__all__'


class FullDocumentDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ('__all__')
