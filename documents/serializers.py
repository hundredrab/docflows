from rest_framework import serializers

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=True)

    class Meta:
        model = Document
        fields = '__all__'
