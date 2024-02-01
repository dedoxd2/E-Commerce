import pytest
from django.contrib.auth.models import User


@pytest.fixture
def create_admin_user(django_user_model):
    """
    Return Admin User
    """
    return django_user_model.objects.create_superuser("admin", "a@a.com", "password")
