from django.urls import path
from .views import (
    SupplierCRUDView, SupplierDataView,
    SupplierDeleteView, LocationCRUDView,
    LocationDataView, LocationDeleteView,
    ItemCategoryCRUDView, ItemCategoryDataView, ItemCategoryDeleteView,
    ItemSubcategoryCRUDView, ItemSubcategoryDataView, ItemSubcategoryDeleteView,
    ItemCRUDView, ItemDataView, ItemDeleteView, LoadItemSubcategoriesView, EquipmentCategoryCRUDView,
    EquipmentCategoryDataView, EquipmentCategoryDeleteView, EquipmentSubcategoryCRUDView, EquipmentSubcategoryDataView,
    EquipmentSubcategoryDeleteView, EquipmentCRUDView, EquipmentDataView, EquipmentDeleteView,
    LoadEquipmentSubcategoriesView, PurchaseOrderCreateView, PurchaseOrderDataView, PurchaseOrderItemDataView,
    ApprovePurchaseOrderView, PurchaseOrderUpdateView, ItemRequisitionCreateView, DraftRequisitionDataView,
    ItemRequisitionUpdateView, SubmittedRequisitionDataView, GeneratePDFView, DraftRequisitionDetailView,
    DraftToSubmittedView, SubmittedRequisitionDetailView, ManageStoreRequisitionOrderView,
    ManagePurchaseRequisitionOrderView, GetCategoriesView, GetSubcategoriesView, GetSuppliersView,
    GeneratePurchasePDFView, ApprovedRequisitionDataView, RejectedRequisitionDataView, DepartmentItemQuantityView,
    OrderPageView, OrderDataView, OrderPurchaseDataView, UnderReviewRequisitionDataView, UnderReviewRequisitionDetailView

)

app_name = 'inventory_app'

urlpatterns = [
    # Supplier
    path('suppliers/', SupplierCRUDView.as_view(), name='supplier'),
    path('ajax_datatable/supplier/', SupplierDataView.as_view(), name='supplier_data'),
    path('supplier/delete/', SupplierDeleteView.as_view(), name='supplier_delete'),

    path('get_suppliers/', GetSuppliersView.as_view(), name='get_suppliers'),

    # Location
    path('warehouse/', LocationCRUDView.as_view(), name='location'),
    path('ajax_datatable/location/', LocationDataView.as_view(), name='location_data'),
    path('location/delete/', LocationDeleteView.as_view(), name='location_delete'),

    # ItemCategory
    path('item_categories/', ItemCategoryCRUDView.as_view(), name='item_category'),
    path('ajax_datatable/item_category/', ItemCategoryDataView.as_view(), name='item_category_data'),
    path('item_category/delete/', ItemCategoryDeleteView.as_view(), name='item_category_delete'),

    path('get_categories/', GetCategoriesView.as_view(), name='get_categories'),

    # ItemSubcategory
    path('item_subcategories/', ItemSubcategoryCRUDView.as_view(), name='item_subcategory'),
    path('ajax_datatable/item_subcategory/', ItemSubcategoryDataView.as_view(), name='item_subcategory_data'),
    path('item_subcategory/delete/', ItemSubcategoryDeleteView.as_view(), name='item_subcategory_delete'),

    path('get_subcategories/', GetSubcategoriesView.as_view(), name='get_subcategories'),

    # Item
    path('items/', ItemCRUDView.as_view(), name='item'),
    path('ajax_datatable/item/', ItemDataView.as_view(), name='item_data'),
    path('item/delete/', ItemDeleteView.as_view(), name='item_delete'),

    # Item Dependent chain
    path('ajax/load-item-subcategories/', LoadItemSubcategoriesView.as_view(), name='ajax_load_item_subcategories'),

    # EquipmentCategory
    path('equipment_categories/', EquipmentCategoryCRUDView.as_view(), name='equipment_category'),
    path('ajax_datatable/equipment_category/', EquipmentCategoryDataView.as_view(), name='equipment_category_data'),
    path('equipment_category/delete/', EquipmentCategoryDeleteView.as_view(), name='equipment_category_delete'),

    # EquipmentSubcategory
    path('equipment_subcategories/', EquipmentSubcategoryCRUDView.as_view(), name='equipment_subcategory'),
    path('ajax_datatable/equipment_subcategory/', EquipmentSubcategoryDataView.as_view(),
         name='equipment_subcategory_data'),
    path('equipment_subcategory/delete/', EquipmentSubcategoryDeleteView.as_view(),
         name='equipment_subcategory_delete'),

    # Equipment
    path('equipment/', EquipmentCRUDView.as_view(), name='equipment'),
    path('ajax_datatable/equipment/', EquipmentDataView.as_view(), name='equipment_data'),
    path('equipment/delete/', EquipmentDeleteView.as_view(), name='equipment_delete'),

    # Equipment Dependent chain
    path('ajax/load-equipment-subcategories/', LoadEquipmentSubcategoriesView.as_view(),
         name='ajax_load_equipment_subcategories'),

    # *****************************************************************************
    # ITEM REQUISITION
    # *****************************************************************************

    path('requisition_order/new/', ItemRequisitionCreateView.as_view(), name='requisition_order_new'),

    # Ajax Tables
    path('ajax_datatable/requisitions/draft/', DraftRequisitionDataView.as_view(), name='draft_requisition_data'),
    path('ajax_datatable/requisitions/submitted/', SubmittedRequisitionDataView.as_view(),
         name='submitted_requisition_data'),
    path('ajax_datatable/requisitions/under-review/', UnderReviewRequisitionDataView.as_view(),
         name='under-review_requisition_data'),
    path('ajax_datatable/requisitions/approved/', ApprovedRequisitionDataView.as_view(),
         name='processed_requisition_data'),
    path('ajax_datatable/requisitions/rejected/', RejectedRequisitionDataView.as_view(),
         name='rejected_requisition_data'),

    path('requisition_order/edit/<int:id>/', ItemRequisitionUpdateView.as_view(), name='requisition_order_edit'),

    # PDF
    path('generate_preview_purchase/<int:requisition_id>/', GeneratePurchasePDFView.as_view(),
         name='generate_preview_purchase'),
    path('generate_preview_store/<int:requisition_id>/', GeneratePurchasePDFView.as_view(),
         name='generate_preview_store'),
    path('generate_preview/<int:requisition_id>/', GeneratePDFView.as_view(), name='generate_preview'),

    # Modals Details
    path('draft_requisitions/<int:pk>/details/', DraftRequisitionDetailView.as_view(),
         name='draft_requisition_details'),
    path('submitted_requisitions/<int:pk>/details/', SubmittedRequisitionDetailView.as_view(),
         name='submitted_requisition_details'),
    path('under-review_requisitions/<int:pk>/details/', UnderReviewRequisitionDetailView.as_view(),
         name='under-review_requisition_details'),

    # Save Draft as Submitted
    path('requisition/<int:id>/submit/', DraftToSubmittedView.as_view(), name='draft_to_submitted'),

    # Manage Store Requisition
    path('store_requisition_order/manage/<int:id>/', ManageStoreRequisitionOrderView.as_view(),
         name='store_requisition_order_manage'),

    # Manage Purchase Requisition
    path('purchase_requisition_order/manage/<int:id>/', ManagePurchaseRequisitionOrderView.as_view(),
         name='purchase_requisition_order_manage'),

    # Department Item Quantity
    path('get_department_item_quantity/', DepartmentItemQuantityView.as_view(), name='get_department_item_quantity'),

    # ORDERS

    path('orders/', OrderPageView.as_view(), name='orders'),
    path('orders/table/', OrderDataView.as_view(), name='orders_table'),
    path('purchase/orders/table/', OrderPurchaseDataView.as_view(), name='purchase_orders_table'),

    # Item Purchase
    path('purchase_order/new/', PurchaseOrderCreateView.as_view(), name='purchase_order_new'),
    path('ajax_datatable/purchased/items/', PurchaseOrderItemDataView.as_view(), name='purchased-item_data'),
    path('ajax_datatable/purchased/orders/', PurchaseOrderDataView.as_view(), name='purchased-order_data'),
    path('purchase_order/<int:id>/approve/', ApprovePurchaseOrderView.as_view(), name='approve_purchase_order'),
    path('purchase_order/edit/<int:id>/', PurchaseOrderUpdateView.as_view(), name='purchase_order_edit'),
]
