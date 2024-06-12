from rest_framework import serializers

from app.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "title", "content", "status", "created_at", "updated_at"]


class DocumentCreateUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False)
    content = serializers.CharField(required=False)
    status = serializers.CharField(required=False)

    class Meta:
        model = Document
        fields = ["pk", "title", "content", "status", "created_at", "updated_at"]
        read_only_fields = ["pk", "status", "created_at", "updated_at"]
