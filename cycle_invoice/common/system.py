"""Class to manage some system operations."""
from django.contrib.auth import get_user_model

def get_system_user():
    """Return the system user, creating it if it does not exist."""
    User = get_user_model()
    user, _ = User.objects.get_or_create(
        username="system",
        defaults={
            "email": "system@buffetitservices.ch",
            "is_active": False,
        },
    )
    return user