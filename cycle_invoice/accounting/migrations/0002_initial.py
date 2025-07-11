# Generated by Django 5.2.2 on 2025-06-20 19:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounting', '0001_initial'),
        ('sale', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpayment',
            name='invoice',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='sale.documentinvoice', verbose_name='invoice'),
        ),
        migrations.AddField(
            model_name='historicalpayment',
            name='updated_by',
            field=models.ForeignKey(blank=True, db_constraint=False, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaltransaction',
            name='account_from',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accounting.account', verbose_name='account from'),
        ),
        migrations.AddField(
            model_name='historicaltransaction',
            name='account_to',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accounting.account', verbose_name='account to'),
        ),
        migrations.AddField(
            model_name='historicaltransaction',
            name='created_by',
            field=models.ForeignKey(blank=True, db_constraint=False, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaltransaction',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaltransaction',
            name='updated_by',
            field=models.ForeignKey(blank=True, db_constraint=False, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transaction',
            name='account_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions_from', to='accounting.account', verbose_name='account from'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='account_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions_to', to='accounting.account', verbose_name='account to'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='created_by',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transaction',
            name='updated_by',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.transaction')),
                ('payment_method', models.CharField(max_length=50, verbose_name='payment method')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sale.documentinvoice', verbose_name='invoice')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
            bases=('accounting.transaction',),
        ),
    ]
