# Generated by Django 5.2.2 on 2025-06-20 19:38

import django.db.models.deletion
import simple_history.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contact', '0001_initial'),
        ('product', '0001_initial'),
        ('subscription', '0001_initial'),
        ('vehicle', '0001_initial'),
        ('work', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('soft_deleted', models.BooleanField(default=False)),
                ('invoice_number', models.CharField(max_length=255, unique=True, verbose_name='invoice number')),
                ('date', models.DateField(verbose_name='date')),
                ('due_date', models.DateField(verbose_name='due date')),
                ('header_text', models.TextField(blank=True, verbose_name='header text')),
                ('footer_text', models.TextField(blank=True, verbose_name='footer text')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_invoice', to='contact.customer')),
                ('updated_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
            },
        ),
        migrations.CreateModel(
            name='HistoricalDocumentInvoice',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('soft_deleted', models.BooleanField(default=False)),
                ('invoice_number', models.CharField(db_index=True, max_length=255, verbose_name='invoice number')),
                ('date', models.DateField(verbose_name='date')),
                ('due_date', models.DateField(verbose_name='due date')),
                ('header_text', models.TextField(blank=True, verbose_name='header text')),
                ('footer_text', models.TextField(blank=True, verbose_name='footer text')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='contact.customer')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, db_constraint=False, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Invoice',
                'verbose_name_plural': 'historical Invoices',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalDocumentItem',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('soft_deleted', models.BooleanField(default=False)),
                ('item_type', models.CharField(choices=[('product', 'Product'), ('subscription', 'Subscription'), ('work', 'Work'), ('expense_vehicle', 'Vehicle expense')], max_length=20, verbose_name='Type')),
                ('price', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='price')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='quantity')),
                ('discount', models.DecimalField(decimal_places=4, default=0, max_digits=5, verbose_name='discount percent')),
                ('comment_title', models.CharField(blank=True, default='', max_length=255, verbose_name='comment title')),
                ('comment_description', models.TextField(blank=True, default='', verbose_name='comment')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='contact.customer')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('invoice', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='sale.documentinvoice')),
                ('product', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='product.product')),
                ('subscription', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='subscription.subscription')),
                ('updated_by', models.ForeignKey(blank=True, db_constraint=False, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='vehicle.vehicle')),
                ('work_type', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='work.worktype')),
            ],
            options={
                'verbose_name': 'historical document item',
                'verbose_name_plural': 'historical document items',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='DocumentItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('soft_deleted', models.BooleanField(default=False)),
                ('item_type', models.CharField(choices=[('product', 'Product'), ('subscription', 'Subscription'), ('work', 'Work'), ('expense_vehicle', 'Vehicle expense')], max_length=20, verbose_name='Type')),
                ('price', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='price')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='quantity')),
                ('discount', models.DecimalField(decimal_places=4, default=0, max_digits=5, verbose_name='discount percent')),
                ('comment_title', models.CharField(blank=True, default='', max_length=255, verbose_name='comment title')),
                ('comment_description', models.TextField(blank=True, default='', verbose_name='comment')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_customer', to='contact.customer')),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='document_item', to='sale.documentinvoice')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='document_item_product', to='product.product')),
                ('subscription', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='document_item_subscription', to='subscription.subscription')),
                ('updated_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='document_item_vehicle', to='vehicle.vehicle')),
                ('work_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='document_item_work_type', to='work.worktype')),
            ],
            options={
                'constraints': [models.CheckConstraint(condition=models.Q(('item_type__in', ['product', 'subscription', 'work', 'expense_vehicle'])), name='sale_documentitem_validate_item_type'), models.CheckConstraint(condition=models.Q(models.Q(('item_type', 'product'), ('product__isnull', False), ('subscription__isnull', True), ('work_type__isnull', True), ('vehicle__isnull', True), ('comment_title', ''), ('comment_description', '')), models.Q(('item_type', 'product'), _negated=True), _connector='OR'), name='sale_documentitem_fields_match_product'), models.CheckConstraint(condition=models.Q(models.Q(('item_type', 'subscription'), ('subscription__isnull', False), ('product__isnull', False), ('comment_title__isnull', False), models.Q(('comment_title', ''), _negated=True), ('work_type__isnull', True), ('vehicle__isnull', True), ('comment_description', '')), models.Q(('item_type', 'subscription'), _negated=True), _connector='OR'), name='sale_documentitem_fields_match_subscription'), models.CheckConstraint(condition=models.Q(models.Q(('item_type', 'work'), ('work_type__isnull', False), ('comment_title__isnull', False), models.Q(('comment_title', ''), _negated=True), ('product__isnull', True), ('subscription__isnull', True), ('vehicle__isnull', True)), models.Q(('item_type', 'work'), _negated=True), _connector='OR'), name='sale_documentitem_fields_match_work'), models.CheckConstraint(condition=models.Q(models.Q(('item_type', 'expense_vehicle'), ('vehicle__isnull', False), ('comment_title__isnull', False), models.Q(('comment_title', ''), _negated=True), ('comment_description__isnull', False), models.Q(('comment_description', ''), _negated=True), ('product__isnull', True), ('subscription__isnull', True), ('work_type__isnull', True)), models.Q(('item_type', 'expense_vehicle'), _negated=True), _connector='OR'), name='sale_documentitem_fields_match_expense_vehicle')],
            },
        ),
    ]
