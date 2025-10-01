import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def staff_user(db):
    user = User.objects.create_user(
        username="staff",
        email="staff@example.com",
        password="pass12345",
        is_active=True,
        is_staff=True,
    )
    return user


@pytest.fixture
def regular_user(db):
    user = User.objects.create_user(
        username="user",
        email="user@example.com",
        password="pass12345",
        is_active=True,
        is_staff=False,
    )
    return user
