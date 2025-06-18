"""Import faker for generating fake data in tests."""
from faker import Faker
from django.contrib.auth.models import User

faker = Faker()


def create_default_user():
    """Create a default user for testing."""
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
    user, created = user_model.objects.get_or_create(username='createuser', defaults={'password': 'createuser'})
    return user
