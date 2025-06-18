"""Import faker for generating fake data in tests."""
from django.contrib.auth import get_user_model
from faker import Faker

faker = Faker()


def get_default_user() -> get_user_model:
    """Create a default user for testing."""
    user_model = get_user_model()
    user, created = user_model.objects.get_or_create(
        username="default_test_user",
        defaults={
            "password": "default_test_password"
        }
    )
    return user
