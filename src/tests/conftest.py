from django.contrib.auth.models import User
from django_dynamic_fixture import G
import pytest

from app.models import Document


@pytest.mark.django_db
@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
@pytest.mark.django_db
def user():
    return G(User)


@pytest.fixture
@pytest.mark.django_db
def documents():
    return [G(Document) for _ in range(3)]
