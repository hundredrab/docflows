from rest_framework import serializers

from .models import Document, Permission


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = '__all__'
        #exclude = ('file',)


class FullDocumentDetailsSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=True)

    class Meta:
        model = Document
        fields = ('__all__')


class PermissionSerializer(serializers.ModelSerializer):
    document = FullDocumentDetailsSerializer()

    class Meta:
        model = Permission
        fields = ('document', 'id', 'level')
