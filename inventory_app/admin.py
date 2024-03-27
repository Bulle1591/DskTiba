from django.contrib import admin

from .models import (
    Supplier,
    ItemCategory,
    ItemSubcategory,
    Item,
    EquipmentCategory,
    EquipmentSubcategory,
    Equipment,
    PurchaseOrder,
    PurchaseOrderItem,
    StockMovement,
    IssuingRecord,
    OrderingRecord,
    OrderingRecordItem,
    Location,
    InventoryTransaction,
    ApprovalPermission,
    ApprovalAuthority,
    ApprovalAuthorityPermission,
)

admin.site.register(Supplier)
admin.site.register(ItemCategory)
admin.site.register(ItemSubcategory)
admin.site.register(Item)
admin.site.register(EquipmentCategory)
admin.site.register(EquipmentSubcategory)
admin.site.register(Equipment)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)
admin.site.register(StockMovement)
admin.site.register(IssuingRecord)
admin.site.register(OrderingRecord)
admin.site.register(OrderingRecordItem)
admin.site.register(Location)
admin.site.register(InventoryTransaction)
admin.site.register(ApprovalPermission)
admin.site.register(ApprovalAuthority)
admin.site.register(ApprovalAuthorityPermission)
