from rest_framework import serializers

from .models import Document, Permission


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        exclude = ('file',)


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        # exclude = ('document',)
        fields = '__all__'


class FullDocumentDetailsSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=True)

    class Meta:
        model = Document
        fields = ('__all__')
