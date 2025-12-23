from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="created_by",
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=django.db.models.deletion.PROTECT,
                editable=False,
                related_name="%(class)s_created_by",
                null=True,
                blank=True,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="updated_by",
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=django.db.models.deletion.PROTECT,
                editable=False,
                related_name="%(class)s_updated_by",
                null=True,
                blank=True,
            ),
        ),
    ]
