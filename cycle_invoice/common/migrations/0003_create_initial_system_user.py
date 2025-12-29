from django.db import migrations
from django.contrib.auth.hashers import make_password


SYSTEM_EMAIL = "system@cycleinvoice.local"


def create_initial_system_user(apps, schema_editor):
    User = apps.get_model("common", "User")

    email = SYSTEM_EMAIL.lower()
    # Idempotent: if a user with this email exists, ensure desired attributes and metadata
    existing = User.objects.filter(email=email).first()
    if existing:
        # Ensure flags are as desired (no staff/superuser) and fields filled
        updates = {}
        if existing.is_staff:
            updates["is_staff"] = False
        if existing.is_superuser:
            updates["is_superuser"] = False
        if existing.first_name != "System":
            updates["first_name"] = "System"
        if existing.last_name != "User":
            updates["last_name"] = "User"
        if existing.created_by_id is None or existing.updated_by_id is None:
            updates["created_by_id"] = existing.id
            updates["updated_by_id"] = existing.id
        if updates:
            User.objects.filter(pk=existing.pk).update(**updates)
        return

    # Create with unusable password and no flags
    user = User(
        email=email,
        first_name="System",
        last_name="User",
        is_active=True,
        is_staff=False,
        is_superuser=False,
    )
    user.password = make_password(None)  # unusable password
    # created_by/updated_by are temporarily nullable in 0002
    user.save()
    # Now self-attribute created_by/updated_by
    User.objects.filter(pk=user.pk).update(created_by_id=user.pk, updated_by_id=user.pk)


def reverse_noop(apps, schema_editor):
    # Do not delete the system user on reverse; keep data intact
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0002_user_created_updated_nullable"),
    ]

    operations = [
        migrations.RunPython(create_initial_system_user, reverse_noop),
    ]
