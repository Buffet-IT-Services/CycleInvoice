# Generated by Django 5.2.1 on 2025-05-21 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0006_historicalproduct_description_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentitemwork',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='historicaldocumentitemwork',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
    ]
