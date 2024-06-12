import pytest
from rest_framework import status
from django_dynamic_fixture import G
from app.enum import DocumentStatus

from app.models import Document


@pytest.mark.django_db
def test_document_create_ok(api_client, user):
    api_client.force_authenticate(user=user)
    data = {
        "title": "Test title",
        "content": "Some content",
    }
    response = api_client.post(f"/api/v1/document/", data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Document.objects.filter(title=data["title"]).exists()


@pytest.mark.django_db
def test_document_detail_ok(api_client, user):
    api_client.force_authenticate(user=user)
    document = G(Document, author=user)

    response = api_client.get(f"/api/v1/document/{document.pk}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["pk"] == document.pk


@pytest.mark.django_db
def test_documents_list_ok(api_client, user, documents):
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/api/v1/document/list/")
    assert response.status_code == status.HTTP_200_OK
    assert documents[0].id in [doc["id"] for doc in response.data]


@pytest.mark.django_db
class TestDocumentArchive:
    def test_archive_document_ok(self, api_client, user):
        api_client.force_authenticate(user=user)
        document = G(Document, author=user)
        response = api_client.delete(f"/api/v1/document/{document.id}/archive/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        document.refresh_from_db()
        assert document.status == DocumentStatus.ARCHIVED.name

    def test_archive_document_not_ok(self, api_client, user):
        api_client.force_authenticate(user=user)
        document = G(Document)
        response = api_client.delete(f"/api/v1/document/{document.id}/archive/")

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestDocumentUpdate:
    def test_update_document_ok(self, api_client, user):
        api_client.force_authenticate(user=user)
        document = G(Document, author=user, title="Title#1")
        new_title = "Title#2"
        response = api_client.patch(
            f"/api/v1/document/{document.id}/", data={"title": new_title}
        )

        assert response.status_code == status.HTTP_200_OK
        document.refresh_from_db()
        assert document.title == new_title

    def test_update_document_not_ok(self, api_client, user):
        api_client.force_authenticate(user=user)
        document = G(Document, title="Title#1")
        response = api_client.patch(
            f"/api/v1/document/{document.id}/", data={"title": "Title"}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_archived_status_not_ok(self, api_client, user):
        api_client.force_authenticate(user=user)
        document = G(Document, status=DocumentStatus.ARCHIVED.name, title="Title#1")
        response = api_client.patch(
            f"/api/v1/document/{document.id}/",
            data={"status": DocumentStatus.PUBLISHED.name},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
