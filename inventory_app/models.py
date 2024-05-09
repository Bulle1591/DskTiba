from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import EmailValidator
from django.db.models import CASCADE
from django.db import transaction
from django.db.models import F
from django.utils import timezone

# GenericForeignKey. This allows a model to have a foreign key to any model, which can be useful in situations like
# yours where a field can relate to more than one model.
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db.models.signals import pre_save
from django.dispatch import receiver


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(validators=[EmailValidator()], blank=True)
    address = models.TextField(blank=True)
    additional_details = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(blank=True, null=True)  # Optional capacity field
    department = models.ForeignKey('hr_app.Department', on_delete=models.CASCADE)
    sub_department = models.ForeignKey('hr_app.SubDepartmentMaster', on_delete=models.SET_NULL, null=True,
                                       blank=True)  # Optional sub-department

    def __str__(self):
        return self.name


class ItemCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ItemSubcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('ItemCategory', on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    ITEM_TYPES = [
        ('product', 'Product'),
        ('service', 'Service'),
    ]
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES, default='product')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    quantity_on_hand = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(blank=True, default=20)
    alert_quantity = models.PositiveIntegerField(blank=True, default=20)
    unit_of_measure = models.CharField(max_length=50)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey('ItemCategory', on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey('ItemSubcategory', on_delete=models.SET_NULL, null=True, blank=True)

    # Additional item-specific attributes
    TABLET = 'TB'
    CAPSULE = 'CP'
    SYRUP = 'SY'
    INJECTION = 'IN'
    CREAM = 'CR'
    OINTMENT = 'OI'
    SUPPOSITORY = 'SU'
    LOZENGE = 'LO'
    PATCH = 'PA'
    AEROSOL = 'AE'

    DOSAGE_FORM_CHOICES = [
        ('', 'Select Dosage Form'),
        (TABLET, 'Tablet'),
        (CAPSULE, 'Capsule'),
        (SYRUP, 'Syrup'),
        (INJECTION, 'Injection'),
        (CREAM, 'Cream'),
        (OINTMENT, 'Ointment'),
        (SUPPOSITORY, 'Suppository'),
        (LOZENGE, 'Lozenge'),
        (PATCH, 'Patch'),
        (AEROSOL, 'Aerosol'),
    ]
    brand_name = models.CharField(max_length=255, blank=True)
    dosage_form = models.CharField(
        max_length=2,
        choices=DOSAGE_FORM_CHOICES,
        default=TABLET,
    )
    strength = models.CharField(max_length=255, blank=True)
    requires_prescription = models.BooleanField(default=False)
    can_be_sold = models.BooleanField(default=False)
    storage_conditions = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = not self.pk  # Check if this is a new object
        super().save(*args, **kwargs)  # Call the "real" save() method

        if is_new:
            # If this is a new object, create a DepartmentInventory object for it
            DepartmentInventory.objects.create(item=self, quantity=0)
            # You can set the department and sub_department according to your needs


class EquipmentSubcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('EquipmentCategory', on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class EquipmentCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    quantity_on_hand = models.PositiveIntegerField(default=0)
    manufacturer = models.CharField(max_length=255, blank=True)
    model_number = models.CharField(max_length=255, blank=True)
    serial_number = models.CharField(max_length=255, unique=True)  # Ensure unique serial numbers
    warranty_information = models.TextField(blank=True)
    maintenance_schedule = models.TextField(blank=True)
    usage_instructions = models.TextField(blank=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey('EquipmentCategory', on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey('EquipmentSubcategory', on_delete=models.SET_NULL, null=True, blank=True)
    IN_USE = 'in_use'
    UNDER_MAINTENANCE = 'under_maintenance'
    DECOMMISSIONED = 'decommissioned'

    STATUS_CHOICES = [
        (IN_USE, 'In Use'),
        (UNDER_MAINTENANCE, 'Under Maintenance'),
        (DECOMMISSIONED, 'Decommissioned'),
    ]

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=IN_USE)
    additional_details = models.TextField(blank=True)

    def __str__(self):
        return self.name


# Model represents all created requisitions (Both Store & Purchase).
class ItemRequisition(models.Model):
    requisition_id = models.CharField(max_length=255, blank=True, null=True)
    REQUISITION_TYPE_CHOICES = [
        ('store', 'Store'),
        ('purchase', 'Purchase'),
    ]
    requisition_type = models.CharField(max_length=20, choices=REQUISITION_TYPE_CHOICES, default='store')
    purchase_order = models.ForeignKey('PurchaseOrder', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True)
    sub_department = models.ForeignKey('hr_app.SubDepartmentMaster', on_delete=models.SET_NULL, null=True)
    requested_by = models.ForeignKey('auth_app.AppUser', on_delete=models.SET_NULL, null=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    SUBMISSION_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
    ]
    submission_status = models.CharField(max_length=20, choices=SUBMISSION_STATUS_CHOICES, default='draft')
    APPROVAL_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('under-review', 'Under Review'),
    ]
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, default='pending')
    approval_status_changed_at = models.DateTimeField(null=True, blank=True)
    approval_status_changed_by = models.ForeignKey('auth_app.AppUser', on_delete=models.SET_NULL, null=True,
                                                   related_name='status_changer')
    agree_to_terms = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super(ItemRequisition, self).save(*args, **kwargs)

    # Signal to update approval_status_changed_at field
    @receiver(pre_save, sender='inventory_app.ItemRequisition')
    def update_status_change_time(sender, instance, **kwargs):
        try:
            obj = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            pass  # Initial save -- do nothing
        else:
            if not obj.approval_status == instance.approval_status and instance.approval_status in ['rejected',
                                                                                                    'approved',
                                                                                                    'under-review']:  # Field has changed
                instance.approval_status_changed_at = timezone.now()
                instance.approval_status_changed_by = instance.current_user  # current logged in user

    def __str__(self):
        if self.requisition_type == 'store' and self.location is not None:
            return f"Store Requisition {self.requisition_id} for {self.location.name}"
        elif self.requisition_type == 'purchase' and self.supplier is not None:
            return f"Purchase Requisition {self.requisition_id} for {self.supplier.name}"
        else:
            return f"Requisition {self.requisition_id}"


# Model represents all items in as specific created requisitions (Both Store & Purchase).
class ItemRequisitionItem(models.Model):
    item_requisition = models.ForeignKey('ItemRequisition', on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    approved_quantity = models.PositiveIntegerField(default=0, blank=True)
    received_quantity = models.PositiveIntegerField(default=0, blank=True)
    remark = models.TextField(blank=True, null=True)  # Add this line

    def __str__(self):
        return f"{self.quantity} of {self.item.name} for requisition {self.item_requisition.id}"


# Model represents counts for requisitions (Both Store & Purchase).
class DailyItemRequisitionCount(models.Model):
    date = models.DateField(unique=True)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.count} requisitions on {self.date}"


# Model represents an order placed for a requisition (Both Store & Purchase).
class ItemOrder(models.Model):
    requisition = models.OneToOneField('ItemRequisition', on_delete=models.CASCADE)
    ordered_by = models.ForeignKey('auth_app.AppUser', on_delete=models.SET_NULL, null=True)
    sub_department = models.ForeignKey('hr_app.SubDepartmentMaster', on_delete=models.SET_NULL, null=True)
    ordered_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    SUBMISSION_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
    ]
    submission_status = models.CharField(max_length=20, choices=SUBMISSION_STATUS_CHOICES, default='draft')
    APPROVAL_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order for {self.requisition}"


# Model represents an items in order placed for a requisition (Both Store & Purchase).
class StoreOrderItem(models.Model):
    item_order = models.ForeignKey('ItemOrder', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    received_quantity = models.PositiveIntegerField(default=0, blank=True)


class PurchaseOrder(models.Model):
    order_id = models.CharField(max_length=255, null=True, editable=True, unique=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    items = models.ManyToManyField('Item', through='PurchaseOrderItem', blank=True)
    equipment = models.ManyToManyField('Equipment', through='PurchaseOrderEquipment', blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_date = models.DateField(auto_now_add=True)
    expected_delivery_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=(
        ('draft', 'Draft'),
        ('fulfilled', 'Fulfilled'),
    ), default='draft')  # Set default to draft

    def __str__(self):
        return f"PO #{self.order_id} - {self.supplier.name}"

    def save(self, *args, **kwargs):
        if not self.order_id:
            date = timezone.now().date()
            daily_order_count, created = DailyPurchaseOrderCount.objects.get_or_create(date=date)
            daily_order_count.count += 1
            daily_order_count.save()
            self.order_id = f"PO-{daily_order_count.count:03d}{date.strftime('%m%d%Y')}"
        super().save(*args, **kwargs)

    # Separate Approve_order method from pending to fulfilled
    @transaction.atomic
    def approve_order(self):
        if self.status == 'fulfilled':
            total_cost = 0
            stock_movements = []
            inventory_transactions = []

            for purchase_order_item in self.items.all():
                # Update quantity_on_hand in Item model
                item = purchase_order_item.item
                item.quantity_on_hand = F('quantity_on_hand') + purchase_order_item.quantity

                # Calculate total cost
                total_cost += purchase_order_item.unit_price * purchase_order_item.quantity

                # Prepare data for StockMovement
                stock_movements.append(
                    StockMovement(
                        item=item,
                        quantity=purchase_order_item.quantity,
                        movement_type='receipt',
                        source=purchase_order_item.location,
                        destination=purchase_order_item.location,
                        purpose='Receipt'
                    )
                )

                # Prepare data for InventoryTransaction
                inventory_transactions.append(
                    InventoryTransaction(
                        item=item,
                        location=purchase_order_item.location,
                        transaction_type='purchase',
                        quantity=purchase_order_item.quantity,
                    )
                )

            # Save total cost in PurchaseOrder
            self.total_cost = total_cost
            self.save()

            # Bulk update items and create StockMovement and InventoryTransaction records
            Item.objects.bulk_update([poi.item for poi in self.items.all()], ['quantity_on_hand'])
            StockMovement.objects.bulk_create(stock_movements)
            InventoryTransaction.objects.bulk_create(inventory_transactions)


class DailyPurchaseOrderCount(models.Model):
    date = models.DateField(unique=True)
    count = models.PositiveIntegerField(default=0)


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey('PurchaseOrder', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # Ensure at least 1 item is ordered
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateField(blank=True, null=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = (('purchase_order', 'item'),)

    def __str__(self):
        return self.item.name


class PurchaseOrderEquipment(models.Model):
    purchase_order = models.ForeignKey('PurchaseOrder', on_delete=models.CASCADE)
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # Ensure at least 1 equipment is ordered
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(blank=True, null=True)
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = (
            ('purchase_order', 'equipment'),)  # Ensure unique combination of purchase order and equipment


class StockMovement(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.IntegerField()  # Can be positive or negative for receipts or issuances
    movement_type = models.CharField(max_length=50, choices=(
        ('receipt', 'Receipt'),
        ('issuance', 'Issuance'),
        ('adjustment', 'Adjustment'),
        ('transfer', 'Transfer'),
    ))
    source_content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    source_object_id = models.PositiveIntegerField()
    source_content_object = GenericForeignKey('source_content_type', 'source_object_id')
    destination = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, related_name='stock_movements_to')
    date_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth_app.AppUser', on_delete=models.SET_NULL, null=True,
                             blank=True)
    purpose = models.TextField(blank=True)

    def __str__(self):
        return f"{self.movement_type} - {self.item.name} ({self.quantity})"


class InventoryTransaction(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=50, choices=(
        ('purchase', 'Purchase'),
        ('usage', 'Usage'),
        ('transfer', 'Transfer'),
        ('adjustment', 'Adjustment'),
    ))
    quantity = models.IntegerField()  # Can be positive or negative for inflows and outflows
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey('auth_app.AppUser', on_delete=models.SET_NULL, null=True,
                             blank=True)  # Optional foreign key to AppUser model

    def __str__(self):
        return f"{self.transaction_type} - {self.item.name} ({self.quantity}) at {self.location.name}"


class DepartmentInventory(models.Model):
    department = models.ForeignKey('hr_app.Department', on_delete=models.CASCADE, null=True, blank=True)
    sub_department = models.ForeignKey('hr_app.SubDepartmentMaster', on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        if self.department is None:
            return f"{self.item.name} (No department assigned) ({self.quantity})"
        else:
            return f"{self.item.name} in {self.department.name} ({self.quantity})"

    @classmethod
    def get_quantity(cls, item, sub_department):
        try:
            inventory = cls.objects.get(item=item, sub_department=sub_department)
            return inventory.quantity
        except cls.DoesNotExist:
            return 0


class IssuingRecord(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity_issued = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # Ensure at least 1 item is issued
    recipient = models.CharField(max_length=255)  # Can be department name or individual name
    date_time = models.DateTimeField(auto_now_add=True)
    purpose = models.TextField(blank=True)
    approver = models.ForeignKey('auth_app.AppUser', on_delete=models.SET_NULL, null=True,
                                 blank=True, related_name='approved_issuing_records')
    issuer = models.ForeignKey('auth_app.AppUser', on_delete=models.SET_NULL, null=True,
                               blank=True, related_name='issued_issuing_records')
    date_time_approved = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=(
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ), default='pending')

    def __str__(self):
        return f"Issuing #{self.issuing_id} - {self.item.name} ({self.quantity_issued}) to {self.recipient}"


class OrderingRecord(models.Model):
    requesting_department = models.CharField(max_length=255)
    items = models.ManyToManyField('Item',
                                   through='OrderingRecordItem')  # ManyToMany relationship with Item through OrderingRecordItem
    date_time = models.DateTimeField(auto_now_add=True)
    approver = models.ForeignKey('auth_app.AppUser', on_delete=models.SET_NULL, null=True,
                                 blank=True, related_name='approved_ordering_records')
    issuer = models.ForeignKey('auth_app.AppUser', on_delete=models.SET_NULL, null=True,
                               blank=True, related_name='issued_ordering_records')
    date_time_approved = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=(
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ), default='pending')

    def __str__(self):
        return f"Order #{self.order_id} - {self.requesting_department}"


class OrderingRecordItem(models.Model):
    ordering_record = models.ForeignKey('OrderingRecord', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = (('ordering_record', 'item'),)


class ApprovalPermission(models.Model):
    permission_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.permission_name


class ApprovalAuthority(models.Model):
    user = models.ForeignKey('auth_app.AppUser', on_delete=models.CASCADE)
    department = models.ForeignKey('hr_app.Department', on_delete=models.CASCADE)
    permissions = models.ManyToManyField('ApprovalPermission', through='ApprovalAuthorityPermission')

    def __str__(self):
        return f"{self.user.username} - {self.department.name} Approvals"


class ApprovalAuthorityPermission(models.Model):
    approval_authority = models.ForeignKey('ApprovalAuthority', on_delete=models.CASCADE)
    permission = models.ForeignKey('ApprovalPermission', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('approval_authority', 'permission'),)
