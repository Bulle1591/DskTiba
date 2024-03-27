from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import EmailValidator
from django.db.models import CASCADE



class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(validators=[EmailValidator()], blank=True)
    address = models.TextField(blank=True)
    additional_details = models.TextField(blank=True)

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
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    quantity_on_hand = models.PositiveIntegerField(default=0)
    unit_of_measure = models.CharField(max_length=50)
    expiration_date = models.DateField(blank=True, null=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey('ItemCategory', on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey('ItemSubcategory', on_delete=models.SET_NULL, null=True, blank=True)

    # Additional item-specific attributes
    dosage = models.CharField(max_length=255, blank=True)
    storage_conditions = models.TextField(blank=True)
    maintenance_schedule = models.TextField(blank=True)
    warranty_information = models.TextField(blank=True)
    usage_instructions = models.TextField(blank=True)

    def __str__(self):
        return self.name


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
    unit_of_measure = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=255, blank=True)
    model_number = models.CharField(max_length=255, blank=True)
    serial_number = models.CharField(max_length=255, unique=True)  # Ensure unique serial numbers
    purchase_date = models.DateField(blank=True, null=True)
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    warranty_information = models.TextField(blank=True)
    maintenance_schedule = models.TextField(blank=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=50, choices=(  # Define choices for equipment status
        ('in_use', 'In Use'),
        ('under_maintenance', 'Under Maintenance'),
        ('decommissioned', 'Decommissioned'),
    ), default='in_use')
    additional_details = models.TextField(blank=True)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    items = models.ManyToManyField('Item', through='PurchaseOrderItem')  # ManyToMany relationship with Item through PurchaseOrderItem
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_date = models.DateField(auto_now_add=True)
    expected_delivery_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=(
        ('pending', 'Pending'),
        ('fulfilled', 'Fulfilled'),
        ('canceled', 'Canceled'),
    ), default='pending')

    def __str__(self):
        return f"PO #{self.order_id} - {self.supplier.name}"


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey('PurchaseOrder', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # Ensure at least 1 item is ordered
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = (('purchase_order', 'item'),)  # Ensure unique combination of purchase order and item


class StockMovement(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.IntegerField()  # Can be positive or negative for receipts or issuances
    movement_type = models.CharField(max_length=50, choices=(
        ('receipt', 'Receipt'),
        ('issuance', 'Issuance'),
        ('adjustment', 'Adjustment'),
        ('transfer', 'Transfer'),
    ))
    source_destination = models.CharField(max_length=255, blank=True)  # Can be supplier name, department name, or location name depending on movement type
    date_time = models.DateTimeField(auto_now_add=True)
    purpose = models.TextField(blank=True)

    def __str__(self):
        return f"{self.movement_type} - {self.item.name} ({self.quantity})"


class IssuingRecord(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity_issued = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # Ensure at least 1 item is issued
    recipient = models.CharField(max_length=255)  # Can be department name or individual name
    date_time = models.DateTimeField(auto_now_add=True)
    purpose = models.TextField(blank=True)
    approver = models.ForeignKey('auth_app.AppUser', on_delete=models.SET_NULL, null=True, blank=True)  # ForeignKey to AppUser model (optional)
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
    items = models.ManyToManyField('Item', through='OrderingRecordItem')  # ManyToMany relationship with Item through OrderingRecordItem
    date_time = models.DateTimeField(auto_now_add=True)
    approver = models.ForeignKey('auth_app.AppUser', on_delete=models.SET_NULL, null=True, blank=True)  # ForeignKey to AppUser model (optional)
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
        unique_together = (('ordering_record', 'item'),)  # Ensure unique combination of ordering record and item


class Location(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(blank=True, null=True)  # Optional capacity field
    department = models.ForeignKey('hr_app.Department', on_delete=models.CASCADE)
    sub_department = models.ForeignKey('hr_app.SubDepartmentMaster', on_delete=models.SET_NULL, null=True, blank=True)  # Optional sub-department

    def __str__(self):
        return self.name


class InventoryTransaction(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=50, choices=(
        ('purchase', 'Purchase'),
        ('usage', 'Usage'),
        ('transfer', 'Transfer'),
        ('adjustment', 'Adjustment'),  # Optional for manual stock adjustments
    ))
    quantity = models.IntegerField()  # Can be positive or negative for inflows and outflows
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey('auth_app.AppUser', on_delete=models.SET_NULL, null=True, blank=True)  # Optional foreign key to AppUser model

    def __str__(self):
        return f"{self.transaction_type} - {self.item.name} ({self.quantity}) at {self.location.name}"



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
