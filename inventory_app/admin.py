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
    ApprovalAuthorityPermission, DailyPurchaseOrderCount, DailyItemRequisitionCount, ItemRequisitionItem,
    ItemRequisition, StoreOrderItem, ItemOrder, DepartmentInventory,
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
admin.site.register(StoreOrderItem)


@admin.register(ItemRequisition)
class ItemRequisitionAdmin(admin.ModelAdmin):
    list_display = ['requisition_id', 'requisition_type', 'purchase_order', 'supplier', 'location', 'sub_department',
                    'requested_by', 'requested_at',
                    'description', 'submission_status', 'approval_status', 'approval_status_changed_by',
                    'agree_to_terms']
    search_fields = ['requisition_id', 'location__name', 'sub_department__name', 'requested_by__name']
    list_filter = ['submission_status', 'approval_status']


@admin.register(ItemRequisitionItem)
class ItemRequisitionItemAdmin(admin.ModelAdmin):
    list_display = ['item_requisition', 'item', 'quantity', 'approved_quantity', 'received_quantity', 'remark']
    search_fields = ['item__name', 'item_requisition__requisition_id']
    list_filter = ['item_requisition__submission_status']


@admin.register(DailyItemRequisitionCount)
class DailyItemRequisitionCountAdmin(admin.ModelAdmin):
    list_display = ['date', 'count']
    search_fields = ['date']


class DailyPurchaseOrderCountAdmin(admin.ModelAdmin):
    list_display = ['date', 'count']


admin.site.register(DailyPurchaseOrderCount, DailyPurchaseOrderCountAdmin)


class ItemOrderAdmin(admin.ModelAdmin):
    list_display = ('requisition', 'ordered_by', 'sub_department', 'ordered_at', 'submission_status', 'approval_status')
    list_filter = ('submission_status', 'approval_status')
    search_fields = ('requisition__item__name', 'ordered_by__user__username')


admin.site.register(ItemOrder, ItemOrderAdmin)


class DepartmentInventoryAdmin(admin.ModelAdmin):
    list_display = ('item', 'department', 'sub_department', 'quantity')
    search_fields = ['item__name', 'department__name', 'sub_department__name']


admin.site.register(DepartmentInventory, DepartmentInventoryAdmin)
