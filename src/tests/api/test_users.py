from django.contrib.auth.models import User
from rest_framework import status
import pytest
import jwt

from app.settings import SECRET_KEY


@pytest.fixture
def auth_url() -> str:
    return "/api/v1/users/token/"


@pytest.fixture
def user_with_pass(user):
    user.set_password("PASSWORD")
    user.save()
    return user


@pytest.mark.django_db
class TestAuthAPI:

    def test_auth_get_token(self, api_client, user_with_pass, auth_url):

        data = {"username": user_with_pass.username, "password": "PASSWORD"}
        response = api_client.post(auth_url, data=data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["access"]
        assert response.data["refresh"]

        payload = jwt.decode(response.data["access"], SECRET_KEY, algorithms=["HS256"])

        assert payload["user_id"] == user_with_pass.pk

    def test_auth_refresh_token(self, api_client, user_with_pass, auth_url):
        data = {"username": user_with_pass.username, "password": "PASSWORD"}
        response = api_client.post(auth_url, data=data, format="json")

        refresh_token = response.data["refresh"]
        url = f"{auth_url}refresh/"
        response = api_client.post(url, data={"refresh": refresh_token}, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["access"]


@pytest.mark.django_db
class TestUserCreate:
    def test_user_create_ok(self, api_client):

        data = {
            "username": "new_username",
            "password": "new_password",
            "email": "example@email.com",
        }
        response = api_client.post(f"/api/v1/users/register/", data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(pk=response.data["id"]).exists()

    def test_user_create_not_ok(self, api_client):

        data = {
            "username": "username",
            "password": "password",
        }
        response = api_client.post(f"/api/v1/users/register/", data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
