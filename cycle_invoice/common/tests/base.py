"""Import faker for generating fake data in tests."""
from django.contrib.auth import get_user_model
from faker import Faker

faker = Faker()


def get_default_test_user(username: str = "default_test_user") -> get_user_model:
    """
    Create a default user for testing.

    :param username: The username for the user to be created or retrieved. Default is "default_test_user".

    :return: A user instance, creating it if it does not exist.
    """
    user_model = get_user_model()
    return user_model.objects.get_or_create(
        username=username,
        defaults={
            "password": username
        }
    )[0]
