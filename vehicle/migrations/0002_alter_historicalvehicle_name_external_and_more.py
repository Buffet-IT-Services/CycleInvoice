# Generated by Django 5.2.1 on 2025-06-07 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalvehicle',
            name='name_external',
            field=models.CharField(max_length=50, verbose_name='external name'),
        ),
        migrations.AlterField(
            model_name='historicalvehicle',
            name='name_internal',
            field=models.CharField(db_index=True, max_length=255, verbose_name='internal name'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='name_external',
            field=models.CharField(max_length=50, verbose_name='external name'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='name_internal',
            field=models.CharField(max_length=255, unique=True, verbose_name='internal name'),
        ),
    ]
