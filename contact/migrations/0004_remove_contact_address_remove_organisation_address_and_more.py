# Generated by Django 5.2.1 on 2025-05-20 21:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0003_alter_customer_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='address',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='address',
        ),
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='organisations', to='contact.address', verbose_name='address'),
        ),
        migrations.AddField(
            model_name='historicalcustomer',
            name='address',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='contact.address', verbose_name='address'),
        ),
    ]
