# Generated by Django 5.0.3 on 2024-04-30 05:22

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('hr_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovalPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DailyItemRequisitionCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('count', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='DailyPurchaseOrderCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('count', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(choices=[('product', 'Product'), ('service', 'Service')], default='product', max_length=10)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('quantity_on_hand', models.PositiveIntegerField(default=0)),
                ('reorder_level', models.PositiveIntegerField(blank=True, default=20)),
                ('alert_quantity', models.PositiveIntegerField(blank=True, default=20)),
                ('unit_of_measure', models.CharField(max_length=50)),
                ('dosage_form', models.CharField(choices=[('TB', 'Tablet'), ('CP', 'Capsule'), ('SY', 'Syrup'), ('IN', 'Injection'), ('CR', 'Cream'), ('OI', 'Ointment'), ('SU', 'Suppository'), ('LO', 'Lozenge'), ('PA', 'Patch'), ('AE', 'Aerosol')], default='TB', max_length=2)),
                ('strength', models.CharField(blank=True, max_length=255)),
                ('requires_prescription', models.BooleanField(default=False)),
                ('can_be_sold', models.BooleanField(default=False)),
                ('storage_conditions', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=255, null=True, unique=True)),
                ('total_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('order_date', models.DateField(auto_now_add=True)),
                ('expected_delivery_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('fulfilled', 'Fulfilled')], default='draft', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('contact_person', models.CharField(blank=True, max_length=255)),
                ('contact_number', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, validators=[django.core.validators.EmailValidator()])),
                ('address', models.TextField(blank=True)),
                ('additional_details', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApprovalAuthority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr_app.department')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ApprovalAuthorityPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_authority', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.approvalauthority')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.approvalpermission')),
            ],
            options={
                'unique_together': {('approval_authority', 'permission')},
            },
        ),
        migrations.AddField(
            model_name='approvalauthority',
            name='permissions',
            field=models.ManyToManyField(through='inventory_app.ApprovalAuthorityPermission', to='inventory_app.approvalpermission'),
        ),
        migrations.CreateModel(
            name='EquipmentSubcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.equipmentcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('quantity_on_hand', models.PositiveIntegerField(default=0)),
                ('manufacturer', models.CharField(blank=True, max_length=255)),
                ('model_number', models.CharField(blank=True, max_length=255)),
                ('serial_number', models.CharField(max_length=255, unique=True)),
                ('warranty_information', models.TextField(blank=True)),
                ('maintenance_schedule', models.TextField(blank=True)),
                ('usage_instructions', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('in_use', 'In Use'), ('under_maintenance', 'Under Maintenance'), ('decommissioned', 'Decommissioned')], default='in_use', max_length=50)),
                ('additional_details', models.TextField(blank=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory_app.equipmentcategory')),
                ('subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory_app.equipmentsubcategory')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory_app.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='IssuingRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_issued', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('recipient', models.CharField(max_length=255)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('purpose', models.TextField(blank=True)),
                ('date_time_approved', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=50)),
                ('approver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_issuing_records', to=settings.AUTH_USER_MODEL)),
                ('issuer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='issued_issuing_records', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory_app.itemcategory'),
        ),
        migrations.CreateModel(
            name='ItemRequisition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requisition_id', models.CharField(blank=True, max_length=255, null=True)),
                ('requisition_type', models.CharField(choices=[('store', 'Store'), ('purchase', 'Purchase')], default='store', max_length=20)),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True)),
                ('submission_status', models.CharField(choices=[('draft', 'Draft'), ('submitted', 'Submitted')], default='draft', max_length=20)),
                ('approval_status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('agree_to_terms', models.BooleanField(default=False)),
                ('requested_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('sub_department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr_app.subdepartmentmaster')),
            ],
        ),
        migrations.CreateModel(
            name='ItemOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True)),
                ('submission_status', models.CharField(choices=[('draft', 'Draft'), ('submitted', 'Submitted')], default='draft', max_length=20)),
                ('approval_status', models.CharField(choices=[('pending', 'Pending'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr_app.department')),
                ('ordered_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr_app.employee')),
                ('requisition', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.itemrequisition')),
            ],
        ),
        migrations.CreateModel(
            name='ItemRequisitionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('approved_quantity', models.PositiveIntegerField(default=0)),
                ('remark', models.TextField(blank=True, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.item')),
                ('item_requisition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='inventory_app.itemrequisition')),
            ],
        ),
        migrations.CreateModel(
            name='ItemSubcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.itemcategory')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory_app.itemsubcategory'),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('capacity', models.PositiveIntegerField(blank=True, null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr_app.department')),
                ('sub_department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr_app.subdepartmentmaster')),
            ],
        ),
        migrations.AddField(
            model_name='itemrequisition',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory_app.location'),
        ),
        migrations.CreateModel(
            name='InventoryTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('purchase', 'Purchase'), ('usage', 'Usage'), ('transfer', 'Transfer'), ('adjustment', 'Adjustment')], max_length=50)),
                ('quantity', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.item')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.location')),
            ],
        ),
        migrations.CreateModel(
            name='OrderingRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requesting_department', models.CharField(max_length=255)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('date_time_approved', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=50)),
                ('approver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_ordering_records', to=settings.AUTH_USER_MODEL)),
                ('issuer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='issued_ordering_records', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderingRecordItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.item')),
                ('ordering_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.orderingrecord')),
            ],
            options={
                'unique_together': {('ordering_record', 'item')},
            },
        ),
        migrations.AddField(
            model_name='orderingrecord',
            name='items',
            field=models.ManyToManyField(through='inventory_app.OrderingRecordItem', to='inventory_app.item'),
        ),
        migrations.AddField(
            model_name='itemrequisition',
            name='purchase_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory_app.purchaseorder'),
        ),
        migrations.CreateModel(
            name='PurchaseOrderEquipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('purchase_date', models.DateField(blank=True, null=True)),
                ('purchase_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.equipment')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory_app.location')),
                ('purchase_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.purchaseorder')),
            ],
            options={
                'unique_together': {('purchase_order', 'equipment')},
            },
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='equipment',
            field=models.ManyToManyField(blank=True, through='inventory_app.PurchaseOrderEquipment', to='inventory_app.equipment'),
        ),
        migrations.CreateModel(
            name='PurchaseOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.item')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory_app.location')),
                ('purchase_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.purchaseorder')),
            ],
            options={
                'unique_together': {('purchase_order', 'item')},
            },
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='items',
            field=models.ManyToManyField(blank=True, through='inventory_app.PurchaseOrderItem', to='inventory_app.item'),
        ),
        migrations.CreateModel(
            name='StockMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('movement_type', models.CharField(choices=[('receipt', 'Receipt'), ('issuance', 'Issuance'), ('adjustment', 'Adjustment'), ('transfer', 'Transfer')], max_length=50)),
                ('source_object_id', models.PositiveIntegerField()),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('purpose', models.TextField(blank=True)),
                ('destination', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stock_movements_to', to='inventory_app.location')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.item')),
                ('source_content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubDepartmentItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_on_hand', models.PositiveIntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.item')),
                ('sub_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr_app.subdepartmentmaster')),
            ],
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.supplier'),
        ),
        migrations.AddField(
            model_name='itemrequisition',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory_app.supplier'),
        ),
        migrations.AddField(
            model_name='item',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory_app.supplier'),
        ),
    ]
