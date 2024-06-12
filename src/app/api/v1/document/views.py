from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from app.api.v1.document.serializers import (
    DocumentCreateUpdateSerializer,
    DocumentSerializer,
)
from app.enum import DocumentStatus
from app.models import Document
from app.permissions import IsAuthorOrReadOnly
from app.filters import DocumentFilter


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DocumentFilter
    serializer_class_map = {
        "create": {
            "request": DocumentCreateUpdateSerializer,
            "response": DocumentSerializer,
        },
        "list": {
            "response": DocumentSerializer,
        },
    }

    @swagger_auto_schema(
        tags=["document"],
        operation_summary="Create document",
        request_body=DocumentCreateUpdateSerializer(),
        responses={
            status.HTTP_201_CREATED: DocumentSerializer(),
            status.HTTP_400_BAD_REQUEST: "Invalid data",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @swagger_auto_schema(
        tags=["document"],
        operation_summary="List documents",
        responses={status.HTTP_200_OK: DocumentSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["document"],
        operation_summary="Destroy document",
        responses={
            status.HTTP_204_NO_CONTENT: "Document deleted successfully",
            status.HTTP_404_NOT_FOUND: "Document not found",
        },
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.status = DocumentStatus.ARCHIVED.name
        instance.save()


class DocumentDetailUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentCreateUpdateSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_status = request.data.get("status")

        if new_status and instance.status != new_status:
            if (
                instance.status == DocumentStatus.PUBLISHED.name
                and new_status == DocumentStatus.DRAFT.name
            ):
                return Response(
                    {
                        "error": 'You cannot change the status from "Published" to "Draft".'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif instance.status == DocumentStatus.ARCHIVED.name:
                return Response(
                    {"error": "You cannot change the status of archived document."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["document"],
        operation_summary="Update document",
        request_body=DocumentCreateUpdateSerializer(),
        responses={
            status.HTTP_200_OK: DocumentSerializer(),
            status.HTTP_400_BAD_REQUEST: "Invalid data",
            status.HTTP_404_NOT_FOUND: "Document not found",
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["document"],
        operation_summary="Partial update document",
        request_body=DocumentCreateUpdateSerializer(),
        responses={
            status.HTTP_200_OK: DocumentSerializer(),
            status.HTTP_400_BAD_REQUEST: "Invalid data",
            status.HTTP_404_NOT_FOUND: "Document not found",
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["document"],
        operation_summary="Retrieve document",
        responses={
            status.HTTP_200_OK: DocumentSerializer(),
            status.HTTP_404_NOT_FOUND: "Document not found",
        },
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
