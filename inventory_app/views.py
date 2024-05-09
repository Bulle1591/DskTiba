import os
import traceback
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from django.forms import formset_factory, inlineformset_factory, model_to_dict
from django.shortcuts import render, get_object_or_404
import json

os.add_dll_directory(r"C:\\Program Files\\GTK3-Runtime Win64\\bin")
from weasyprint import HTML

from xhtml2pdf import pisa  # Using xhtml2pdf
from io import BytesIO
from django.template.loader import get_template, render_to_string
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView

from auth_app.models import AppUser
from hr_app.models import Employee, SubDepartmentMaster, EmployeeContact
from .forms import SupplierForm, LocationForm, ItemCategoryForm, ItemSubcategoryForm, ItemForm, EquipmentCategoryForm, \
    EquipmentSubcategoryForm, EquipmentForm, PurchaseOrderForm, PurchaseOrderItemForm, ItemRequisitionForm, \
    ItemRequisitionItemForm
from .models import Supplier, Location, ItemCategory, ItemSubcategory, Item, EquipmentCategory, EquipmentSubcategory, \
    Equipment, PurchaseOrder, DailyPurchaseOrderCount, PurchaseOrderItem, StockMovement, InventoryTransaction, \
    ItemRequisition, DailyItemRequisitionCount, ItemRequisitionItem, StoreOrderItem, ItemOrder, DepartmentInventory


# ///////////////////////////////////////////////////////
# ////////// SUPPLIER
class SupplierCRUDView(View):
    template_name = "inventory_app/supplier/list.html"

    def get(self, request, *args, **kwargs):
        form = SupplierForm()
        context = {
            'form': form,
            # Add any other context variables you need
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        supplier_id = request.POST.get('id')
        name = request.POST.get('name')
        # Add any other fields you need

        if supplier_id:
            supplier = Supplier.objects.get(id=supplier_id)
            if Supplier.objects.filter(name__iexact=name).exclude(id=supplier_id).exists():
                self.response = {"message": 'Supplier with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = SupplierForm(request.POST, instance=supplier)
                success_message = 'Supplier updated successfully!'
        else:
            if Supplier.objects.filter(name__iexact=name).exists():
                self.response = {"message": 'Supplier with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = SupplierForm(request.POST)
                success_message = 'Supplier created successfully!'

        if form.is_valid():
            form.save()
            self.response = {"message": success_message, "success": True}
            return JsonResponse(self.response)

        context = {
            'form': form,
            # Add any other context variables you need
        }
        return render(request, self.template_name, context)


class SupplierDataView(View):
    def get(self, request, *args, **kwargs):
        # Query all data
        data = Supplier.objects.all()

        # Format the data for DataTables
        data_for_datatables = [{
            'id': supplier.id,
            'name': supplier.name,
            'contact_person': supplier.contact_person,
            'contact_number': supplier.contact_number,
            'email': supplier.email,
            'address': supplier.address,
            'additional_details': supplier.additional_details,
        } for supplier in data]

        # Return the data
        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),  # The draw counter for DataTables
            'recordsTotal': len(data_for_datatables),  # The total number of records
            'recordsFiltered': len(data_for_datatables),  # The number of records after filtering
            'data': data_for_datatables,  # The data to display
        })


class SupplierDeleteView(View):
    def post(self, request, *args, **kwargs):
        # Get the IDs from the request
        ids = request.POST.getlist('ids[]')

        # Delete the Supplier objects with the given IDs
        Supplier.objects.filter(id__in=ids).delete()

        # Return a success response with a message
        return JsonResponse({
            'success': True,
            'message': 'Selection have been successfully deleted!'
        })


class GetSuppliersView(View):
    def get(self, request, *args, **kwargs):
        suppliers = [{'id': supplier.id, 'name': supplier.name} for supplier in Supplier.objects.all()]
        return JsonResponse(suppliers, safe=False)


# ///////////////////////////////////////////////////////
# ////////// LOCATION

class LocationCRUDView(View):
    template_name = "inventory_app/location/list.html"

    def get(self, request, *args, **kwargs):
        form = LocationForm()
        context = {
            'form': form,
            # Add any other context variables you need
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        location_id = request.POST.get('id')
        name = request.POST.get('name')
        # Add any other fields you need

        if location_id:
            location = Location.objects.get(id=location_id)
            if Location.objects.filter(name__iexact=name).exclude(id=location_id).exists():
                self.response = {"message": 'Location with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = LocationForm(request.POST, instance=location)
                success_message = 'Location updated successfully!'
        else:
            if Location.objects.filter(name__iexact=name).exists():
                self.response = {"message": 'Location with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = LocationForm(request.POST)
                success_message = 'Location created successfully!'

        if form.is_valid():
            form.save()
            self.response = {"message": success_message, "success": True}
            return JsonResponse(self.response)

        context = {
            'form': form,
            # Add any other context variables you need
        }
        return render(request, self.template_name, context)


class LocationDataView(View):
    def get(self, request, *args, **kwargs):
        # Query all data
        data = Location.objects.all()

        # Format the data for DataTables
        data_for_datatables = [{
            'id': location.id,
            'name': location.name,
            'capacity': location.capacity,
            'department': location.department.name if location.department else '',
            'department_id': location.department.id if location.department else None,
            'sub_department': location.sub_department.name if location.sub_department else '',
            'sub_department_id': location.sub_department.id if location.sub_department else None,
        } for location in data]

        # Return the data
        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),  # The draw counter for DataTables
            'recordsTotal': len(data_for_datatables),  # The total number of records
            'recordsFiltered': len(data_for_datatables),  # The number of records after filtering
            'data': data_for_datatables,  # The data to display
        })


class LocationDeleteView(View):
    def post(self, request, *args, **kwargs):
        # Get the IDs from the request
        ids = request.POST.getlist('ids[]')

        # Delete the Location objects with the given IDs
        Location.objects.filter(id__in=ids).delete()

        # Return a success response with a message
        return JsonResponse({
            'success': True,
            'message': 'Selection have been successfully deleted!'
        })


# ///////////////////////////////////////////////////////
# ////////// ITEM CATEGORY

class ItemCategoryCRUDView(View):
    template_name = "inventory_app/item/category/list.html"

    def get(self, request, *args, **kwargs):
        form = ItemCategoryForm()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        category_id = request.POST.get('id')
        name = request.POST.get('name')

        if category_id:
            category = ItemCategory.objects.get(id=category_id)
            if ItemCategory.objects.filter(name__iexact=name).exclude(id=category_id).exists():
                self.response = {"message": 'Item Category with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = ItemCategoryForm(request.POST, instance=category)
                success_message = 'Item Category updated successfully!'
        else:
            if ItemCategory.objects.filter(name__iexact=name).exists():
                self.response = {"message": 'Item Category with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = ItemCategoryForm(request.POST)
                success_message = 'Item Category created successfully!'

        if form.is_valid():
            form.save()
            self.response = {"message": success_message, "success": True}
            return JsonResponse(self.response)

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class ItemCategoryDataView(View):
    def get(self, request, *args, **kwargs):
        data = ItemCategory.objects.all()
        data_for_datatables = [{
            'id': category.id,
            'name': category.name,
            'description': category.description,
        } for category in data]

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': len(data_for_datatables),
            'recordsFiltered': len(data_for_datatables),
            'data': data_for_datatables,
        })


class ItemCategoryDeleteView(View):
    def post(self, request, *args, **kwargs):
        ids = request.POST.getlist('ids[]')
        ItemCategory.objects.filter(id__in=ids).delete()

        return JsonResponse({
            'success': True,
            'message': 'Selection have been successfully deleted!'
        })


class GetCategoriesView(View):
    def get(self, request, *args, **kwargs):
        categories = [{'id': category.id, 'name': category.name} for category in ItemCategory.objects.all()]
        return JsonResponse(categories, safe=False)


# ///////////////////////////////////////////////////////
# ////////// ITEM SUB CATEGORY
class ItemSubcategoryCRUDView(View):
    template_name = "inventory_app/item/subcategory/list.html"

    def get(self, request, *args, **kwargs):
        form = ItemSubcategoryForm()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        subcategory_id = request.POST.get('id')
        name = request.POST.get('name')
        category_id = request.POST.get('category')

        if subcategory_id:
            subcategory = ItemSubcategory.objects.get(id=subcategory_id)
            if ItemSubcategory.objects.filter(name__iexact=name).exclude(id=subcategory_id).exists():
                self.response = {"message": 'Item Subcategory with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = ItemSubcategoryForm(request.POST, instance=subcategory)
                success_message = 'Item Subcategory updated successfully!'
        else:
            if ItemSubcategory.objects.filter(name__iexact=name).exists():
                self.response = {"message": 'Item Subcategory with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = ItemSubcategoryForm(request.POST)
                success_message = 'Item Subcategory created successfully!'

        if form.is_valid():
            form.save()
            self.response = {"message": success_message, "success": True}
            return JsonResponse(self.response)

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class ItemSubcategoryDataView(View):
    def get(self, request, *args, **kwargs):
        data = ItemSubcategory.objects.all()
        data_for_datatables = [{
            'id': subcategory.id,
            'name': subcategory.name,
            'description': subcategory.description,
            'category': subcategory.category.name if subcategory.category else '',
            'category_id': subcategory.category.id if subcategory.category else None,
        } for subcategory in data]

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': len(data_for_datatables),
            'recordsFiltered': len(data_for_datatables),
            'data': data_for_datatables,
        })


class ItemSubcategoryDeleteView(View):
    def post(self, request, *args, **kwargs):
        ids = request.POST.getlist('ids[]')
        ItemSubcategory.objects.filter(id__in=ids).delete()

        return JsonResponse({
            'success': True,
            'message': 'Selection have been successfully deleted!'
        })


class GetSubcategoriesView(View):
    def get(self, request, *args, **kwargs):
        subcategories = [{'id': subcategory.id, 'name': subcategory.name} for subcategory in
                         ItemSubcategory.objects.all()]
        return JsonResponse(subcategories, safe=False)


# ///////////////////////////////////////////////////////
# ////////// ITEM

class ItemCRUDView(View):
    template_name = "inventory_app/item/list.html"

    def get(self, request, *args, **kwargs):
        form = ItemForm()

        # Get item types, categories, subcategories, and dosage forms
        item_types = Item.ITEM_TYPES
        categories = ItemCategory.objects.all()
        subcategories = ItemSubcategory.objects.all()
        dosage_forms = Item.DOSAGE_FORM_CHOICES

        context = {
            'form': form,
            'item_types': item_types,
            'categories': categories,
            'subcategories': subcategories,
            'dosage_forms': dosage_forms,
            # Add any other context variables you need
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('id')
        name = request.POST.get('name')
        # Add any other fields you need

        if item_id:
            item = Item.objects.get(id=item_id)
            if Item.objects.filter(name__iexact=name).exclude(id=item_id).exists():
                self.response = {"message": 'Item with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = ItemForm(request.POST, instance=item)
                success_message = 'Item updated successfully!'
        else:
            if Item.objects.filter(name__iexact=name).exists():
                self.response = {"message": 'Item with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = ItemForm(request.POST)
                success_message = 'Item created successfully!'

        if form.is_valid():
            form.save()
            self.response = {"message": success_message, "success": True}
            return JsonResponse(self.response)

        # Get item types, categories, subcategories, and dosage forms
        item_types = Item.ITEM_TYPES
        categories = ItemCategory.objects.all()
        subcategories = ItemSubcategory.objects.all()
        dosage_forms = Item.DOSAGE_FORM_CHOICES

        context = {
            'form': form,
            'item_types': item_types,
            'categories': categories,
            'subcategories': subcategories,
            'dosage_forms': dosage_forms,
            # Add any other context variables you need
        }
        return render(request, self.template_name, context)


# Item Category and Item Subcategory dependent or “chained” select fields
class LoadItemSubcategoriesView(View):
    def get(self, request):
        category_id = request.GET.get('category_id')
        print(f"Category ID: {category_id}")  # print the category_id to the console

        subcategories = ItemSubcategory.objects.filter(category__id=category_id).order_by('name')
        print(f"Subcategories: {subcategories}")  # print the subcategories to the console

        subcategory_list = list(subcategories.values('id', 'name'))
        print(f"Subcategory List: {subcategory_list}")  # print the subcategory_list to the console

        return JsonResponse(subcategory_list, safe=False)


class ItemDataView(View):
    def get(self, request, *args, **kwargs):
        # Initial queryset
        queryset = Item.objects.all()

        # Search item query
        search_query = request.GET.get('search_query')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        # Filter by item type
        item_type = request.GET.get('item_type')
        if item_type:
            queryset = queryset.filter(item_type=item_type)

        # Filter by category
        category_id = request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

            # If category is Pharmaceuticals, filter by dosage form
            category = ItemCategory.objects.get(id=category_id)
            if category.name == 'Pharmaceuticals':
                dosage_form = request.GET.get('dosage_form')
                if dosage_form:
                    queryset = queryset.filter(dosage_form=dosage_form)

        # Filter by subcategory
        subcategory_id = request.GET.get('subcategory_id')
        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)

        # Format the filtered data for DataTables
        data_for_datatables = [{
            'id': item.id,
            'name': item.name,
            'item_type_display': item.get_item_type_display(),
            'item_type': item.item_type,
            'description': item.description,
            'quantity_on_hand': item.quantity_on_hand,
            'reorder_level': item.reorder_level,
            'alert_quantity': item.alert_quantity,
            'unit_of_measure': item.unit_of_measure,
            'supplier': item.supplier.name if item.supplier else '',
            'supplier_id': item.supplier.id if item.supplier else None,
            'category': item.category.name if item.category else '',
            'category_id': item.category.id if item.category else None,
            'subcategory': item.subcategory.name if item.subcategory else '',
            'subcategory_id': item.subcategory.id if item.subcategory else None,
            'dosage_form_display': item.get_dosage_form_display(),
            'dosage_form': item.dosage_form,
            'strength': item.strength,
            'brand_name': item.brand_name,
            'requires_prescription': item.requires_prescription,
            'can_be_sold': item.can_be_sold,
            'storage_conditions': item.storage_conditions,
        } for item in queryset]

        # Return the filtered data
        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),  # The draw counter for DataTables
            'recordsTotal': len(data_for_datatables),  # The total number of records
            'recordsFiltered': len(data_for_datatables),  # The number of records after filtering
            'data': data_for_datatables,  # The data to display
        })


class ItemDeleteView(View):
    def post(self, request, *args, **kwargs):
        # Get the IDs from the request
        ids = request.POST.getlist('ids[]')

        # Delete the Item objects with the given IDs
        Item.objects.filter(id__in=ids).delete()

        # Return a success response with a message
        return JsonResponse({
            'success': True,
            'message': 'Selection have been successfully deleted!'
        })


# ///////////////////////////////////////////////////////
# ////////// EQUIPMENT CATEGORY

class EquipmentCategoryCRUDView(View):
    template_name = "inventory_app/equipment/category/list.html"

    def get(self, request, *args, **kwargs):
        form = EquipmentCategoryForm()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        category_id = request.POST.get('id')
        name = request.POST.get('name')

        if category_id:
            category = EquipmentCategory.objects.get(id=category_id)
            if EquipmentCategory.objects.filter(name__iexact=name).exclude(id=category_id).exists():
                self.response = {"message": 'Equipment Category with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = EquipmentCategoryForm(request.POST, instance=category)
                success_message = 'Equipment Category updated successfully!'
        else:
            if EquipmentCategory.objects.filter(name__iexact=name).exists():
                self.response = {"message": 'Equipment Category with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = EquipmentCategoryForm(request.POST)
                success_message = 'Equipment Category created successfully!'

        if form.is_valid():
            form.save()
            self.response = {"message": success_message, "success": True}
            return JsonResponse(self.response)

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class EquipmentCategoryDataView(View):
    def get(self, request, *args, **kwargs):
        data = EquipmentCategory.objects.all()
        data_for_datatables = [{
            'id': category.id,
            'name': category.name,
            'description': category.description,
        } for category in data]

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': len(data_for_datatables),
            'recordsFiltered': len(data_for_datatables),
            'data': data_for_datatables,
        })


class EquipmentCategoryDeleteView(View):
    def post(self, request, *args, **kwargs):
        ids = request.POST.getlist('ids[]')
        EquipmentCategory.objects.filter(id__in=ids).delete()

        return JsonResponse({
            'success': True,
            'message': 'Selection have been successfully deleted!'
        })


# ///////////////////////////////////////////////////////
# ////////// EQUIPMENT SUBCATEGORY
class EquipmentSubcategoryCRUDView(View):
    template_name = "inventory_app/equipment/subcategory/list.html"

    def get(self, request, *args, **kwargs):
        form = EquipmentSubcategoryForm()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        subcategory_id = request.POST.get('id')
        name = request.POST.get('name')

        if subcategory_id:
            subcategory = EquipmentSubcategory.objects.get(id=subcategory_id)
            if EquipmentSubcategory.objects.filter(name__iexact=name).exclude(id=subcategory_id).exists():
                self.response = {"message": 'Equipment Subcategory with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = EquipmentSubcategoryForm(request.POST, instance=subcategory)
                success_message = 'Equipment Subcategory updated successfully!'
        else:
            if EquipmentSubcategory.objects.filter(name__iexact=name).exists():
                self.response = {"message": 'Equipment Subcategory with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = EquipmentSubcategoryForm(request.POST)
                success_message = 'Equipment Subcategory created successfully!'

        if form.is_valid():
            form.save()
            self.response = {"message": success_message, "success": True}
            return JsonResponse(self.response)

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class EquipmentSubcategoryDataView(View):
    def get(self, request, *args, **kwargs):
        data = EquipmentSubcategory.objects.all()
        data_for_datatables = [{
            'id': subcategory.id,
            'name': subcategory.name,
            'description': subcategory.description,
            'category': subcategory.category.name,
        } for subcategory in data]

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': len(data_for_datatables),
            'recordsFiltered': len(data_for_datatables),
            'data': data_for_datatables,
        })


class EquipmentSubcategoryDeleteView(View):
    def post(self, request, *args, **kwargs):
        ids = request.POST.getlist('ids[]')
        EquipmentSubcategory.objects.filter(id__in=ids).delete()

        return JsonResponse({
            'success': True,
            'message': 'Selection have been successfully deleted!'
        })


# ///////////////////////////////////////////////////////
# ////////// EQUIPMENT

class EquipmentCRUDView(View):
    template_name = "inventory_app/equipment/list.html"

    def get(self, request, *args, **kwargs):
        form = EquipmentForm()

        # Get categories, subcategories, and dosage forms
        statuses = Equipment.STATUS_CHOICES
        categories = EquipmentCategory.objects.all()
        subcategories = EquipmentSubcategory.objects.all()

        context = {
            'form': form,
            'statuses': statuses,
            'categories': categories,
            'subcategories': subcategories,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        equipment_id = request.POST.get('id')
        serial_number = request.POST.get('serial_number')

        if equipment_id:
            equipment = Equipment.objects.get(id=equipment_id)
            if Equipment.objects.filter(serial_number__iexact=serial_number).exclude(id=equipment_id).exists():
                self.response = {"message": 'Equipment with this Serial Number already exists.'}
                return JsonResponse(self.response)
            else:
                form = EquipmentForm(request.POST, instance=equipment)
                success_message = 'Equipment updated successfully!'
        else:
            if Equipment.objects.filter(serial_number__iexact=serial_number).exists():
                self.response = {"message": 'Equipment with this Serial Number already exists.'}
                return JsonResponse(self.response)
            else:
                form = EquipmentForm(request.POST)
                success_message = 'Equipment created successfully!'

        if form.is_valid():
            form.save()
            self.response = {"message": success_message, "success": True}
            return JsonResponse(self.response)

        # Get categories, subcategories, and dosage forms
        statuses = Equipment.STATUS_CHOICES
        categories = EquipmentCategory.objects.all()
        subcategories = EquipmentSubcategory.objects.all()

        context = {
            'form': form,
            'statuses': statuses,
            'categories': categories,
            'subcategories': subcategories,
        }
        return render(request, self.template_name, context)


# Equipment Category and Equipment Subcategory dependent or “chained” select fields
class LoadEquipmentSubcategoriesView(View):
    def get(self, request):
        category_id = request.GET.get('category_id')
        print(f"Category ID: {category_id}")  # print the category_id to the console

        subcategories = EquipmentSubcategory.objects.filter(category__id=category_id).order_by('name')
        print(f"Subcategories: {subcategories}")  # print the subcategories to the console

        subcategory_list = list(subcategories.values('id', 'name'))
        print(f"Subcategory List: {subcategory_list}")  # print the subcategory_list to the console

        return JsonResponse(subcategory_list, safe=False)


class EquipmentDataView(View):
    def get(self, request, *args, **kwargs):
        data = Equipment.objects.all()
        data_for_datatables = [{
            'id': equipment.id,
            'name': equipment.name,
            'description': equipment.description,
            'quantity_on_hand': equipment.quantity_on_hand,
            'manufacturer': equipment.manufacturer,
            'model_number': equipment.model_number,
            'serial_number': equipment.serial_number,
            'warranty_information': equipment.warranty_information,
            'maintenance_schedule': equipment.maintenance_schedule,
            'usage_instructions': equipment.usage_instructions,
            'status': equipment.get_status_display(),
            'additional_details': equipment.additional_details,
        } for equipment in data]

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': len(data_for_datatables),
            'recordsFiltered': len(data_for_datatables),
            'data': data_for_datatables,
        })


class EquipmentDeleteView(View):
    def post(self, request, *args, **kwargs):
        ids = request.POST.getlist('ids[]')
        Equipment.objects.filter(id__in=ids).delete()

        return JsonResponse({
            'success': True,
            'message': 'Selection have been successfully deleted!'
        })


# ///////////////////////////////////////////////////////
# ////////// ITEM REQUISITIONS
class ItemRequisitionCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = ItemRequisition
    form_class = ItemRequisitionForm
    template_name = 'inventory_app/item/requisition/create.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        if user.is_authenticated:  # Check if the user is authenticated
            if user.is_superuser:
                form.fields['sub_department'].queryset = SubDepartmentMaster.objects.all()
                # Filter AppUser objects to only include those who are staff and have a role
                form.fields['requested_by'].queryset = AppUser.objects.filter(is_staff=True,
                                                                              role__isnull=False)
            else:
                employee = Employee.objects.filter(user=user).first()
                if employee:
                    form.fields['sub_department'].queryset = SubDepartmentMaster.objects.filter(
                        id=employee.sub_department.id)
                    # Filter AppUser objects to only include those who are staff and have a role
                    form.fields['requested_by'].queryset = AppUser.objects.filter(id=user.id, is_staff=True,
                                                                                  role__isnull=False)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ItemRequisitionFormSet = formset_factory(ItemRequisitionItemForm, extra=0)
        context['item_requisition_item_formset'] = ItemRequisitionFormSet(self.request.POST or None)

        # Calculate the next requisition_id
        date = timezone.now().date()
        daily_requisition_count, created = DailyItemRequisitionCount.objects.get_or_create(date=date)
        next_requisition_id = f"IR-{daily_requisition_count.count + 1:03d}{date.strftime('%m%d%Y')}"
        context['next_requisition_id'] = next_requisition_id

        # Get the current user
        user = self.request.user

        # If the user is a superuser, count all requisitions
        if user.is_superuser or (user.role and user.role.name == 'Procurement Officer'):
            num_draft_requisitions = ItemRequisition.objects.filter(
                Q(submission_status='draft') & Q(approval_status='pending')).count()
            num_submitted_requisitions = ItemRequisition.objects.filter(
                Q(submission_status='submitted') & Q(approval_status='pending')).count()
            num_approved_requisitions = ItemRequisition.objects.filter(approval_status='approved').count()
            num_rejected_requisitions = ItemRequisition.objects.filter(approval_status='rejected').count()
            num_under_review_requisitions = ItemRequisition.objects.filter(approval_status='under-review').count()
        else:
            # If the user is not a superuser, count only the requisitions they created
            num_draft_requisitions = ItemRequisition.objects.filter(
                Q(submission_status='draft') & Q(approval_status='pending') & Q(requested_by=user)).count()
            num_submitted_requisitions = ItemRequisition.objects.filter(
                Q(submission_status='submitted') & Q(approval_status='pending') & Q(requested_by=user)).count()
            num_approved_requisitions = ItemRequisition.objects.filter(
                Q(approval_status='approved') & Q(requested_by=user)).count()
            num_rejected_requisitions = ItemRequisition.objects.filter(
                Q(approval_status='rejected') & Q(requested_by=user)).count()
            num_under_review_requisitions = ItemRequisition.objects.filter(
                Q(approval_status='under-review') & Q(requested_by=user)).count()

        context['num_draft_requisitions'] = num_draft_requisitions
        context['num_submitted_requisitions'] = num_submitted_requisitions
        context['num_approved_requisitions'] = num_approved_requisitions
        context['num_rejected_requisitions'] = num_rejected_requisitions
        context['num_under_review_requisitions'] = num_under_review_requisitions

        # Pass superuser to context
        context['is_superuser'] = self.request.user.is_superuser

        # Pass user_id to context
        context['user_id'] = self.request.user.id

        return context

    @transaction.atomic
    def form_valid(self, form):
        # Check if the user has a draft Store Requisition or Purchase Requisition
        existing_draft_requisition = ItemRequisition.objects.filter(
            requested_by=self.request.user,
            submission_status='draft',
            requisition_type__in=['store', 'purchase']
        ).first()

        # Check if the user has a submitted or pending Store Requisition or Purchase Requisition
        existing_submitted_or_pending_requisition = ItemRequisition.objects.filter(
            requested_by=self.request.user,
            approval_status__in=['pending', 'under-review'],
            requisition_type__in=['store', 'purchase']
        ).first()

        if existing_draft_requisition:
            message = 'You have a draft Requisition. Please complete it before creating a new one.'
            self.response = {"message": message, "success": False}
            return JsonResponse(self.response)

        if existing_submitted_or_pending_requisition:
            if existing_submitted_or_pending_requisition.approval_status == 'pending':
                message = 'You have a pending Requisition. Please wait until it is approved before creating a new one.'
            else:  # existing_submitted_or_pending_requisition.approval_status == 'under-review'
                message = 'You have a Requisition under review. Please wait until it is approved before creating a new one.'
            self.response = {"message": message, "success": False}
            return JsonResponse(self.response)

        context = self.get_context_data(form=form)
        item_requisition_formset = context['item_requisition_item_formset']

        # Create a new requisition
        item_requisition = form.save(commit=False)
        item_requisition.requisition_id = context['next_requisition_id']

        try:
            if all([form.is_valid(), item_requisition_formset.is_valid()]):
                item_requisition.save()

                for form in item_requisition_formset:
                    if form.is_valid():
                        item_requisition_item = form.save(commit=False)
                        item_requisition_item.item_requisition = item_requisition
                        item_requisition_item.save()

                # Set the submission status based on the form action
                action = self.request.POST.get('action')
                if action == 'save-draft':
                    item_requisition.submission_status = 'draft'
                    message = 'Requisition draft saved successfully!'
                elif action == 'submit':
                    item_requisition.submission_status = 'final'
                    message = 'Requisition submitted successfully!'

                item_requisition.save()

                self.response = {"message": message, "success": True}
                return JsonResponse(self.response)

            else:
                form_errors = json.dumps(form.errors)
                formset_errors = json.dumps([form.errors for form in item_requisition_formset])
                self.response = {"message": "Form validation failed", "success": False, "form_errors": form_errors,
                                 "formset_errors": formset_errors}
                return JsonResponse(self.response)

        except Exception as e:
            traceback_str = traceback.format_exc()  # Get the traceback as a string
            self.response = {"message": f"{type(e).__name__}: {str(e)}", "success": False, "traceback": traceback_str}
            return JsonResponse(self.response, status=500)

        context = {
            'form': form,
        }

        return render(self.request, self.template_name, context)


class ItemRequisitionUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = ItemRequisition
    form_class = ItemRequisitionForm
    template_name = 'inventory_app/item/requisition/update.html'

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        return get_object_or_404(ItemRequisition, id=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ItemRequisitionItemFormSet = inlineformset_factory(ItemRequisition, ItemRequisitionItem,
                                                           form=ItemRequisitionItemForm,
                                                           extra=0, can_delete=True)
        context['item_requisition_item_formset'] = ItemRequisitionItemFormSet(self.request.POST or None,
                                                                              instance=self.object)
        context['requisition'] = self.object  # Get id for requisition order
        context['requisition_id'] = self.object.requisition_id  # Get order id for requisition order
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        if user.is_authenticated:  # Check if the user is authenticated
            if user.is_superuser:
                form.fields['sub_department'].queryset = SubDepartmentMaster.objects.all()
                # Filter AppUser objects to only include those who are staff and have a role
                form.fields['requested_by'].queryset = AppUser.objects.filter(is_staff=True,
                                                                              role__isnull=False)
            else:
                employee = Employee.objects.filter(user=user).first()
                if employee:
                    form.fields['sub_department'].queryset = SubDepartmentMaster.objects.filter(
                        id=employee.sub_department.id)
                    # Filter AppUser objects to only include those who are staff and have a role
                    form.fields['requested_by'].queryset = AppUser.objects.filter(id=user.id, is_staff=True,
                                                                                  role__isnull=False)
        return form

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data(form=form)
        item_requisition_formset = context['item_requisition_item_formset']

        try:
            if all([form.is_valid(), item_requisition_formset.is_valid()]):
                item_requisition = form.save(commit=False)

                for form in item_requisition_formset:
                    if form.is_valid():
                        if form.cleaned_data.get('DELETE'):
                            # If the form is marked for deletion, delete the instance
                            form.instance.delete()
                        else:
                            form.save()

                # Set the submission status based on the submitted action
                action = self.request.POST.get('action')
                if action == 'save-draft':
                    item_requisition.submission_status = 'draft'
                elif action == 'submit':
                    item_requisition.submission_status = 'submitted'

                item_requisition.save()  # Now save the requisition with updated status

                message = 'Requisition updated successfully!'
                self.response = {"message": message, "success": True}
                return JsonResponse(self.response)

            else:
                form_errors = json.dumps(form.errors)
                formset_errors = json.dumps([form.errors for form in item_requisition_formset])
                self.response = {"message": "Form validation failed", "success": False, "form_errors": form_errors,
                                 "formset_errors": formset_errors}
                return JsonResponse(self.response)

        except Exception as e:
            traceback_str = traceback.format_exc()  # Get the traceback as a string
            self.response = {"message": f"{type(e).__name__}: {str(e)}", "success": False, "traceback": traceback_str}
            return JsonResponse(self.response, status=500)

        context = {
            'form': form,
        }
        return render(self.request, self.template_name, context)


# Preview Requisition as PDF
class GeneratePDFView(View):

    def get(self, request, requisition_id):
        """
        Processes a PDF generation request based on the provided requisition ID.
        """
        requisition = get_object_or_404(ItemRequisition, pk=requisition_id)

        # Prepare context data for the template
        context = {
            'requisition': requisition,
            'items': requisition.items.all(),
        }

        # Render the HTML template with data
        template = get_template('inventory_app/item/requisition/includes/pdfs/purchase_draft.html')
        html = template.render(context)

        # Generate the PDF using WeasyPrint
        pdf_data = self.generate_pdf_content(html)

        # Create a PDF response without download headers
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Length'] = len(pdf_data)
        response['Content-Disposition'] = 'filename=requisition.pdf'

        return response

    def generate_pdf_content(self, html):
        """
        Generates the PDF content using WeasyPrint.
        """
        html = HTML(string=html)
        pdf_data = html.write_pdf()

        return pdf_data


#############################################################################
# Purchase PDF
class GeneratePurchasePDFView(View):

    def get(self, request, requisition_id):
        """
        Processes a PDF generation request based on the provided requisition ID.
        """
        requisition = get_object_or_404(ItemRequisition, pk=requisition_id)

        # Prepare context data for the template
        context = {
            'requisition': requisition,
            'requisition_items': [{
                "item_name": item.item.name,
                "quantity": item.quantity,
                "remark": item.remark,
                "quantity_on_hand": item.item.quantity_on_hand,
                "quantity_in_sub_department": DepartmentInventory.get_quantity(item.item, requisition.sub_department),
                "strength": item.item.strength,
            } for item in ItemRequisitionItem.objects.filter(item_requisition=requisition)]
        }

        # Render the HTML template with data
        template = get_template('inventory_app/item/requisition/includes/pdfs/purchase_draft.html')
        html = template.render(context)

        # Generate the PDF using WeasyPrint
        pdf_data = self.generate_pdf_content(html)

        # Create a PDF response without download headers
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Length'] = len(pdf_data)
        response['Content-Disposition'] = 'filename=requisition.pdf'

        return response

    def generate_pdf_content(self, html):
        """
        Generates the PDF content using WeasyPrint.
        """
        html = HTML(string=html)
        pdf_data = html.write_pdf()

        return pdf_data


#############################################################################
# Draft Requisitions Table view
class DraftRequisitionDataView(View):
    def get(self, request, *args, **kwargs):
        # Check if the user is a superuser
        if request.user.is_superuser:
            data = ItemRequisition.objects.filter(submission_status='draft')
        else:
            # Filter the drafts by the user who created them
            data = ItemRequisition.objects.filter(submission_status='draft', requested_by=request.user)

        data_for_datatables = [{
            'id': requisition.id,
            'requisition_id': requisition.requisition_id,
            'requisition_type': requisition.get_requisition_type_display(),
            'location': requisition.location.name if requisition.location else None,
            'supplier': requisition.supplier.name if requisition.supplier else None,
            'issuer': requisition.location.name if requisition.requisition_type == 'store' else (
                requisition.supplier.name if requisition.requisition_type == 'purchase' else None),
            'sub_department': requisition.sub_department.name if requisition.sub_department else None,
            'requested_by': requisition.requested_by.full_name,
            'requested_at': requisition.requested_at.strftime('%Y-%m-%d'),
            'submission_status': requisition.get_submission_status_display(),
            'approval_status': requisition.get_approval_status_display(),
            'items': [{
                'item_name': item.item.name,
                'quantity': item.quantity,
            } for item in ItemRequisitionItem.objects.filter(item_requisition=requisition)]
        } for requisition in data]

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': len(data_for_datatables),
            'recordsFiltered': len(data_for_datatables),
            'data': data_for_datatables,
        })


#############################################################################
# Submitted Requisitions Table view
class SubmittedRequisitionDataView(View):
    def get(self, request, *args, **kwargs):

        # Get the current user
        user = self.request.user

        # Check if the user is a superuser or a Procurement Officer
        if user.is_superuser or (user.role and user.role.name == 'Procurement Officer'):
            data = ItemRequisition.objects.filter(submission_status='submitted', approval_status='pending')
        else:
            # Filter the submissions by the user who created them
            data = ItemRequisition.objects.filter(submission_status='submitted', approval_status='pending',
                                                  requested_by=request.user)

        data_for_datatables = [{
            'id': requisition.id,
            'requisition_id': requisition.requisition_id,
            'requisition_type': requisition.get_requisition_type_display(),
            'location': requisition.location.name if requisition.location else None,
            'supplier': requisition.supplier.name if requisition.supplier else None,
            'issuer': requisition.location.name if requisition.requisition_type == 'store' else (
                requisition.supplier.name if requisition.requisition_type == 'purchase' else None),
            'sub_department': requisition.sub_department.name if requisition.sub_department else None,
            'requested_by': requisition.requested_by.full_name,
            'requested_at': requisition.requested_at.strftime('%Y-%m-%d'),
            'submission_status': requisition.get_submission_status_display(),
            'approval_status': requisition.get_approval_status_display(),
            'items': [{
                'item_name': item.item.name,
                'quantity': item.quantity,
                'approved_quantity': item.approved_quantity,
                'quantity_on_hand': item.item.quantity_on_hand,
                'quantity_in_sub_department': DepartmentInventory.get_quantity(item.item, requisition.sub_department),
            } for item in ItemRequisitionItem.objects.filter(item_requisition=requisition)]
        } for requisition in data]

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': len(data_for_datatables),
            'recordsFiltered': len(data_for_datatables),
            'data': data_for_datatables,
        })


#############################################################################
# Under Review Requisitions Table view
class UnderReviewRequisitionDataView(View):
    def get(self, request, *args, **kwargs):

        # Get the current user
        user = self.request.user

        # Check if the user is a superuser
        if user.is_superuser or (user.role and user.role.name == 'Procurement Officer'):
            data = ItemRequisition.objects.filter(approval_status='under-review')
        else:
            # Filter the drafts by the user who created them
            data = ItemRequisition.objects.filter(approval_status='under-review', requested_by=request.user)

        data_for_datatables = [{
            'id': requisition.id,
            'requisition_id': requisition.requisition_id,
            'requisition_type': requisition.get_requisition_type_display(),
            'location': requisition.location.name if requisition.location else None,
            'supplier': requisition.supplier.name if requisition.supplier else None,
            'issuer': requisition.location.name if requisition.requisition_type == 'store' else (
                requisition.supplier.name if requisition.requisition_type == 'purchase' else None),
            'sub_department': requisition.sub_department.name if requisition.sub_department else None,
            'requested_by': requisition.requested_by.full_name,
            'requested_at': requisition.requested_at.strftime('%Y-%m-%d'),
            'submission_status': requisition.get_submission_status_display(),
            'approval_status': requisition.get_approval_status_display(),
            'items': [{
                'item_name': item.item.name,
                'quantity': item.quantity,
                'approved_quantity': item.approved_quantity,
            } for item in ItemRequisitionItem.objects.filter(item_requisition=requisition)]
        } for requisition in data]

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': len(data_for_datatables),
            'recordsFiltered': len(data_for_datatables),
            'data': data_for_datatables,
        })


#############################################################################
# Pending Requisitions Table view
class ApprovedRequisitionDataView(View):
    def get(self, request, *args, **kwargs):
        # Check if the user is a superuser
        if request.user.is_superuser:
            data = ItemRequisition.objects.filter(approval_status='approved')
        else:
            # Filter the drafts by the user who created them
            data = ItemRequisition.objects.filter(approval_status='approved', requested_by=request.user)

        data_for_datatables = [{
            'id': requisition.id,
            'requisition_id': requisition.requisition_id,
            'requisition_type': requisition.get_requisition_type_display(),
            'location': requisition.location.name if requisition.location else None,
            'supplier': requisition.supplier.name if requisition.supplier else None,
            'issuer': requisition.location.name if requisition.requisition_type == 'store' else (
                requisition.supplier.name if requisition.requisition_type == 'purchase' else None),
            'sub_department': requisition.sub_department.name if requisition.sub_department else None,
            'requested_by': requisition.requested_by.full_name,
            'requested_at': requisition.requested_at.strftime('%Y-%m-%d'),
            'submission_status': requisition.get_submission_status_display(),
            'approval_status': requisition.get_approval_status_display(),
            'items': [{
                'item_name': item.item.name,
                'quantity': item.quantity,
                'approved_quantity': item.approved_quantity,
            } for item in ItemRequisitionItem.objects.filter(item_requisition=requisition)]
        } for requisition in data]

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': len(data_for_datatables),
            'recordsFiltered': len(data_for_datatables),
            'data': data_for_datatables,
        })


# Pending Requisitions Table view
class RejectedRequisitionDataView(View):
    def get(self, request, *args, **kwargs):
        # Check if the user is a superuser
        if request.user.is_superuser:
            data = ItemRequisition.objects.filter(approval_status='rejected')
        else:
            # Filter the drafts by the user who created them
            data = ItemRequisition.objects.filter(approval_status='rejected', requested_by=request.user)

        data_for_datatables = [{
            'id': requisition.id,
            'requisition_id': requisition.requisition_id,
            'requisition_type': requisition.get_requisition_type_display(),
            'location': requisition.location.name if requisition.location else None,
            'supplier': requisition.supplier.name if requisition.supplier else None,
            'issuer': requisition.location.name if requisition.requisition_type == 'store' else (
                requisition.supplier.name if requisition.requisition_type == 'purchase' else None),
            'sub_department': requisition.sub_department.name if requisition.sub_department else None,
            'requested_by': requisition.requested_by.full_name,
            'requested_at': requisition.requested_at.strftime('%Y-%m-%d'),
            'submission_status': requisition.get_submission_status_display(),
            'approval_status': requisition.get_approval_status_display(),
            'items': [{
                'item_name': item.item.name,
                'quantity': item.quantity,
                'approved_quantity': item.approved_quantity,
            } for item in ItemRequisitionItem.objects.filter(item_requisition=requisition)]
        } for requisition in data]

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': len(data_for_datatables),
            'recordsFiltered': len(data_for_datatables),
            'data': data_for_datatables,
        })


#############################################################################
# Draft Requisition Details in modal
class DraftRequisitionDetailView(DetailView):
    model = ItemRequisition

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        requisition = self.object
        requested_by_employee = Employee.objects.get(user=requisition.requested_by)
        employee_contact = EmployeeContact.objects.get(employee=requested_by_employee)
        context['requisition_data'] = {
            "id": requisition.id,
            "requisition_type": requisition.get_requisition_type_display(),
            "location": requisition.location.name if requisition.location else None,
            "supplier": requisition.supplier.name if requisition.supplier else None,
            "issuer": requisition.location.name if requisition.requisition_type == 'store' else (
                requisition.supplier.name if requisition.requisition_type == 'purchase' else None),
            "requisition_id": requisition.requisition_id,
            "sub_department": requisition.sub_department.name,
            "requested_by": requisition.requested_by.full_name,
            "email": requisition.requested_by.email,
            "phone_number": employee_contact.phone_number,
            "requested_at": requisition.requested_at.strftime('%Y-%m-%d %H:%M:%S'),
            "description": requisition.description,
            "submission_status": requisition.get_submission_status_display(),
            # Add other relevant data fields
        }
        context['requisition_items'] = [{
            "item_name": item.item.name,
            "quantity": item.quantity,
            "remark": item.remark,
            "quantity_on_hand": item.item.quantity_on_hand,
            "quantity_in_sub_department": DepartmentInventory.get_quantity(item.item, requisition.sub_department),
            "strength": item.item.strength,
        } for item in ItemRequisitionItem.objects.filter(item_requisition=requisition)]
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            html = render_to_string('inventory_app/item/requisition/includes/modals/draft/modal_body.html', context,
                                    request=self.request)
            return HttpResponse(html)
        else:
            return super().render_to_response(context, **response_kwargs)


#############################################################################
# Submitted Requisition Details in modal
class SubmittedRequisitionDetailView(DetailView):
    model = ItemRequisition

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        requisition = self.object
        requested_by_employee = Employee.objects.get(user=requisition.requested_by)
        employee_contact = EmployeeContact.objects.get(employee=requested_by_employee)
        context['requisition_data'] = {
            "id": requisition.id,
            "requisition_type": requisition.get_requisition_type_display(),
            "location": requisition.location.name if requisition.location else None,
            "supplier": requisition.supplier.name if requisition.supplier else None,
            "issuer": requisition.location.name if requisition.requisition_type == 'store' else (
                requisition.supplier.name if requisition.requisition_type == 'purchase' else None),
            "requisition_id": requisition.requisition_id,
            "sub_department": requisition.sub_department.name,
            "requested_by": requisition.requested_by.full_name,
            "email": requisition.requested_by.email,
            "phone_number": employee_contact.phone_number,
            "requested_at": requisition.requested_at.strftime('%Y-%m-%d %H:%M:%S'),
            "description": requisition.description,
            "submission_status": requisition.get_submission_status_display(),
            # Add other relevant data fields
        }
        context['requisition_items'] = [{
            "item_name": item.item.name,
            "quantity": item.quantity,
            "remark": item.remark,
            "quantity_on_hand": item.item.quantity_on_hand,
            "quantity_in_sub_department": DepartmentInventory.get_quantity(item.item, requisition.sub_department),
            "strength": item.item.strength,
        } for item in ItemRequisitionItem.objects.filter(item_requisition=requisition)]
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            html = render_to_string('inventory_app/item/requisition/includes/modals/submitted/modal_body.html', context,
                                    request=self.request)
            return HttpResponse(html)
        else:
            return super().render_to_response(context, **response_kwargs)


#############################################################################
# Under Review Requisition Details in modal
class UnderReviewRequisitionDetailView(DetailView):
    model = ItemRequisition

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        requisition = self.object
        requested_by_employee = Employee.objects.get(user=requisition.requested_by)
        employee_contact = EmployeeContact.objects.get(employee=requested_by_employee)
        context['requisition_data'] = {
            "id": requisition.id,
            "requisition_type": requisition.get_requisition_type_display(),
            "location": requisition.location.name if requisition.location else None,
            "supplier": requisition.supplier.name if requisition.supplier else None,
            "issuer": requisition.location.name if requisition.requisition_type == 'store' else (
                requisition.supplier.name if requisition.requisition_type == 'purchase' else None),
            "requisition_id": requisition.requisition_id,
            "sub_department": requisition.sub_department.name,
            "requested_by": requisition.requested_by.full_name,
            "email": requisition.requested_by.email,
            "phone_number": employee_contact.phone_number,
            "requested_at": requisition.requested_at.strftime('%Y-%m-%d %H:%M:%S'),
            "approval_status": requisition.approval_status,
            "approval_status_changed_by": requisition.approval_status_changed_by.full_name,
            "approval_status_changed_at": requisition.approval_status_changed_at,
            "description": requisition.description,
            "submission_status": requisition.get_submission_status_display(),
            # Add other relevant data fields
        }
        context['requisition_items'] = [{
            "item_name": item.item.name,
            "quantity": item.quantity,
            "remark": item.remark,
            "quantity_on_hand": item.item.quantity_on_hand,
            "approved_quantity": item.approved_quantity,
            "quantity_in_sub_department": DepartmentInventory.get_quantity(item.item, requisition.sub_department),
            "strength": item.item.strength,
        } for item in ItemRequisitionItem.objects.filter(item_requisition=requisition)]
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            html = render_to_string('inventory_app/item/requisition/includes/modals/under-review/modal_body.html', context,
                                    request=self.request)
            return HttpResponse(html)
        else:
            return super().render_to_response(context, **response_kwargs)


#############################################################################
# Submit Requisition from Draft to Submitted
class DraftToSubmittedView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def post(self, request, *args, **kwargs):
        requisition = get_object_or_404(ItemRequisition, id=self.kwargs.get('id'))
        requisition.submission_status = 'submitted'
        requisition.save()
        return JsonResponse({"message": "Requisition submitted successfully for approval!", "success": True})


#############################################################################
# Approve and Reject Store Requisition order
class ManageStoreRequisitionOrderView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = ItemRequisition
    form_class = ItemRequisitionForm
    template_name = 'inventory_app/item/requisition/manage_store_order.html'

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        return get_object_or_404(ItemRequisition, id=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ItemRequisitionItemFormSet = inlineformset_factory(ItemRequisition, ItemRequisitionItem,
                                                           form=ItemRequisitionItemForm,
                                                           extra=0, can_delete=True)
        context['item_requisition_item_formset'] = ItemRequisitionItemFormSet(self.request.POST or None,
                                                                              instance=self.object)
        context['requisition'] = self.object  # Get id for requisition order
        context['requisition_id'] = self.object.requisition_id  # Get order id for requisition order
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        if user.is_authenticated:  # Check if the user is authenticated
            if user.is_superuser:
                form.fields['sub_department'].queryset = SubDepartmentMaster.objects.all()
                # Filter AppUser objects to only include those who are staff and have a role
                form.fields['requested_by'].queryset = AppUser.objects.filter(is_staff=True,
                                                                              role__isnull=False)
            else:
                employee = Employee.objects.filter(user=user).first()
                if employee:
                    form.fields['sub_department'].queryset = SubDepartmentMaster.objects.filter(
                        id=employee.sub_department.id)
                    # Filter AppUser objects to only include those who are staff and have a role
                    form.fields['requested_by'].queryset = AppUser.objects.filter(id=user.id, is_staff=True,
                                                                                  role__isnull=False)
        return form

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data(form=form)
        item_requisition_formset = context['item_requisition_item_formset']

        try:
            if all([form.is_valid(), item_requisition_formset.is_valid()]):
                item_requisition = form.save(commit=False)

                for form in item_requisition_formset:
                    if form.is_valid():
                        form.save()

                # Set the submission status based on the submitted action
                action = self.request.POST.get('action')
                if action in ['approve', 'reject', 'under-review']:
                    item_requisition.approval_status = action
                    item_requisition.approval_status_changed_at = timezone.now()  # import timezone from django.utils
                    item_requisition.approval_status_changed_by = self.request.user

                    # Create an ItemOrder in all cases
                    item_order = ItemOrder.objects.create(
                        requisition=item_requisition,
                        ordered_by=self.request.user.employee,  # Assuming the user model has a related_name 'employee'
                        department=self.request.user.employee.department,
                        # Assuming the Employee model has a 'department' field
                        description=item_requisition.description,
                        submission_status='submitted',
                        approval_status='pending' if action == 'under-review' else 'cancelled' if action == 'reject' else 'delivered'
                    )

                    if action == 'under-review':
                        # Deduct the approved quantity from the item's quantity_on_hand
                        item_requisition.item.quantity_on_hand -= item_requisition.quantity
                        item_requisition.item.save()

                        # Create a StoreOrderItem and associate it with the ItemOrder
                        StoreOrderItem.objects.create(
                            item_order=item_order,
                            item=item_requisition.item,
                            quantity=item_requisition.quantity
                        )
                        # Create a StockMovement
                        StockMovement.objects.create(
                            item=item_requisition.item,
                            quantity=item_requisition.quantity,
                            # Assuming the ItemRequisition model has a 'quantity' field
                            movement_type='issuance',
                            source_content_object=item_order,
                            destination=item_requisition.location,
                            # Assuming the ItemRequisition model has a 'location' field
                            user=self.request.user,
                            purpose=f"{self.request.user.email} approved requisition of {item_requisition.quantity} units of {item_requisition.item.name} from {item_requisition.location} to {item_requisition.sub_department}"
                        )
                        # Create an InventoryTransaction
                        InventoryTransaction.objects.create(
                            item=item_requisition.item,
                            location=item_requisition.location,
                            transaction_type='usage',
                            quantity=-item_requisition.quantity,  # The quantity is negative for 'usage'
                            user=self.request.user
                        )

                item_requisition.save()  # Now save the requisition with updated status

                message = 'Requisition ' + action + ' successfully!'
                self.response = {"message": message, "success": True}
                return JsonResponse(self.response)

            else:
                form_errors = json.dumps(form.errors)
                formset_errors = json.dumps([form.errors for form in item_requisition_formset])
                self.response = {"message": "Form validation failed", "success": False, "form_errors": form_errors,
                                 "formset_errors": formset_errors}
                return JsonResponse(self.response)

        except Exception as e:
            traceback_str = traceback.format_exc()  # Get the traceback as a string
            self.response = {"message": f"{type(e).__name__}: {str(e)}", "success": False, "traceback": traceback_str}
            return JsonResponse(self.response, status=500)

        context = {
            'form': form,
        }
        return render(self.request, self.template_name, context)


#############################################################################
# Approve and Reject Purchase Requisition order
class ManagePurchaseRequisitionOrderView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = ItemRequisition
    form_class = ItemRequisitionForm
    template_name = 'inventory_app/item/requisition/manage_purchase_order.html'

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        return get_object_or_404(ItemRequisition, id=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ItemRequisitionItemFormSet = inlineformset_factory(ItemRequisition, ItemRequisitionItem,
                                                           form=ItemRequisitionItemForm,
                                                           extra=0, can_delete=True)
        context['item_requisition_item_formset'] = ItemRequisitionItemFormSet(self.request.POST or None,
                                                                              instance=self.object)
        context['requisition'] = self.object  # Get id for requisition order
        context['requisition_id'] = self.object.requisition_id  # Get order id for requisition order
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        if user.is_authenticated:  # Check if the user is authenticated
            if user.is_superuser:
                form.fields['sub_department'].queryset = SubDepartmentMaster.objects.all()
                # Filter AppUser objects to only include those who are staff and have a role
                form.fields['requested_by'].queryset = AppUser.objects.filter(is_staff=True,
                                                                              role__isnull=False)
            else:
                employee = Employee.objects.filter(user=user).first()
                if employee:
                    # Set sub department to the original requisition creator
                    form.fields['sub_department'].queryset = SubDepartmentMaster.objects.filter(
                        id=self.object.sub_department.id)
                    # Filter AppUser objects to only include those who are staff and have a role
                    form.fields['requested_by'].queryset = AppUser.objects.filter(id=user.id, is_staff=True,
                                                                                  role__isnull=False)
        return form

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data(form=form)
        item_requisition_formset = context['item_requisition_item_formset']

        try:
            if all([form.is_valid(), item_requisition_formset.is_valid()]):
                item_requisition = form.save(commit=False)

                # Set the submission status based on the submitted action
                action = self.request.POST.get('action')
                try:
                    employee = self.request.user.employee
                except ObjectDoesNotExist:
                    employee = None

                if action in ['approved', 'rejected', 'under-review']:
                    item_requisition.approval_status = action
                    item_requisition.approval_status_changed_at = timezone.now()  # import timezone from django.utils
                    item_requisition.approval_status_changed_by = self.request.user

                    # Create an ItemOrder in all cases
                    item_order = ItemOrder.objects.create(
                        requisition=item_requisition,
                        ordered_by=item_requisition.requested_by,
                        sub_department=item_requisition.sub_department,
                        description=item_requisition.description,
                        submission_status='submitted',
                        approval_status='pending' if action == 'under-review' else 'cancelled' if action == 'reject' else 'processing' if action == 'approved' else 'delivered'
                    )

                    if action == 'approved':
                        # Loop over all ItemRequisitionItem instances related to this ItemRequisition
                        for item_requisition_item in item_requisition.items.all():
                            # Create a StoreOrderItem and associate it with the ItemOrder
                            StoreOrderItem.objects.create(
                                item_order=item_order,
                                item=item_requisition_item.item,
                                quantity=item_requisition_item.quantity
                            )

                # Save the ItemRequisition instance and ItemRequisitionItem instances here
                item_requisition.save()  # Now save the requisition with updated status
                for form in item_requisition_formset:
                    if form.is_valid():
                        form.save()

                message = 'Requisition ' + action + ' successfully!'
                self.response = {"message": message, "success": True}
                return JsonResponse(self.response)

            else:
                form_errors = json.dumps(form.errors)
                formset_errors = json.dumps([form.errors for form in item_requisition_formset])
                self.response = {"message": "Form validation failed", "success": False, "form_errors": form_errors,
                                 "formset_errors": formset_errors}
                return JsonResponse(self.response)

        except Exception as e:
            traceback_str = traceback.format_exc()  # Get the traceback as a string
            self.response = {"message": f"{type(e).__name__}: {str(e)}", "success": False, "traceback": traceback_str}
            return JsonResponse(self.response, status=500)

        context = {
            'form': form,
        }
        return render(self.request, self.template_name, context)


#############################################################################
# Get each department available item quantity
class DepartmentItemQuantityView(View):
    def get(self, request, *args, **kwargs):
        item_id = request.GET.get('item_id')
        user_id = request.GET.get('user_id')

        try:
            item = Item.objects.get(id=item_id)
            user = AppUser.objects.get(id=user_id)
        except (Item.DoesNotExist, AppUser.DoesNotExist):
            return JsonResponse({'quantity': 0})

        department_name = user.employee.department
        try:
            department = SubDepartmentMaster.objects.get(name=department_name)
        except SubDepartmentMaster.DoesNotExist:
            return JsonResponse({'quantity': 0})

        quantity = DepartmentInventory.get_quantity(item, department)
        return JsonResponse({'quantity': quantity})


# Order List page view
class OrderPageView(TemplateView):
    template_name = 'inventory_app/item/orders/lists.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = ItemOrder.objects.all()
        context['total_orders'] = orders.count()
        context['store_orders'] = orders.filter(requisition__requisition_type='store').count()
        context['purchase_orders'] = orders.filter(requisition__requisition_type='purchase').count()
        return context


# Table for all created Orders for Store and Purchase (Order Process)
class OrderDataView(View):
    def get(self, request, *args, **kwargs):
        # Get all the orders
        orders = ItemOrder.objects.all()

        # Prepare the data for the DataTable
        data_for_datatables = self.prepare_data_for_datatables(orders)

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': len(data_for_datatables),
            'recordsFiltered': len(data_for_datatables),
            'data': data_for_datatables,
        })

    def prepare_data_for_datatables(self, orders):
        return [{
            'order_id': order.id,
            'requisition': order.requisition.requisition_id,
            'ordered_by': order.ordered_by.full_name if order.ordered_by else 'N/A',
            'sub_department': order.sub_department.name,
            'ordered_at': order.ordered_at.strftime('%Y-%m-%d'),
            'submission_status': order.get_submission_status_display(),
            'approval_status': order.get_approval_status_display(),
            'items': [{
                'item_name': item.item.name,
                'quantity': item.quantity,
                'approved_quantity': ItemRequisitionItem.objects.get(item=item.item,
                                                                     item_requisition=order.requisition).approved_quantity,
                'quantity_on_hand': item.item.quantity_on_hand,
                'quantity_in_sub_department': DepartmentInventory.get_quantity(item.item,
                                                                               order.requisition.sub_department),
            } for item in StoreOrderItem.objects.filter(item_order=order)]
        } for order in orders]


# Table for all created Orders for Purchase (Procurement - Item Order)
class OrderPurchaseDataView(View):
    def get(self, request, *args, **kwargs):
        # Get all the orders for requisition_type 'purchase'
        orders = ItemOrder.objects.filter(requisition__requisition_type='purchase')

        # Prepare the data for the DataTable
        data_for_datatables = self.prepare_data_for_datatables(orders)

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': len(data_for_datatables),
            'recordsFiltered': len(data_for_datatables),
            'data': data_for_datatables,
        })

    def prepare_data_for_datatables(self, orders):
        return [{
            'order_id': order.id,
            'requisition': order.requisition.requisition_id,
            'ordered_by': order.ordered_by.full_name if order.ordered_by else 'N/A',
            'sub_department': order.sub_department.name,
            'ordered_at': order.ordered_at.strftime('%Y-%m-%d'),
            'submission_status': order.get_submission_status_display(),
            'approval_status': order.get_approval_status_display(),
            'items': [{
                'item_name': item.item.name,
                'quantity': item.quantity,
                'approved_quantity': ItemRequisitionItem.objects.get(item=item.item,
                                                                     item_requisition=order.requisition).approved_quantity,
                'quantity_on_hand': item.item.quantity_on_hand,
                'quantity_in_sub_department': DepartmentInventory.get_quantity(item.item,
                                                                               order.requisition.sub_department),
            } for item in StoreOrderItem.objects.filter(item_order=order)]
        } for order in orders]


# ///////////////////////////////////////////////////////
# ////////// PURCHASE ORDER AND THEIR ITEMS
class PurchaseOrderCreateView(CreateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'inventory_app/item/purchase/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        PurchaseOrderFormSet = formset_factory(PurchaseOrderItemForm, extra=1)
        context['purchase_order_item_formset'] = PurchaseOrderFormSet(self.request.POST or None)

        # Calculate the next order_id
        date = timezone.now().date()
        daily_order_count, created = DailyPurchaseOrderCount.objects.get_or_create(date=date)
        next_order_id = f"PO-{daily_order_count.count + 1:03d}{date.strftime('%m%d%Y')}"
        context['next_order_id'] = next_order_id

        # Count the number of draft purchase orders in the database(Check if there is draft order)
        num_draft_orders = PurchaseOrder.objects.filter(status='draft').count()
        context['num_draft_orders'] = num_draft_orders

        # Pass superuser to context
        context['is_superuser'] = self.request.user.is_superuser

        return context

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data(form=form)
        purchase_order_formset = context['purchase_order_item_formset']

        try:
            if all([form.is_valid(), purchase_order_formset.is_valid()]):
                purchase_order = form.save(commit=False)
                purchase_order.save()

                total_cost = 0
                for form in purchase_order_formset:
                    if form.is_valid():
                        purchase_order_item = form.save(commit=False)
                        purchase_order_item.purchase_order = purchase_order
                        purchase_order_item.save()

                        # Calculate total cost
                        total_cost += purchase_order_item.unit_price * purchase_order_item.quantity

                        if purchase_order.status != 'draft':
                            # Update quantity_on_hand in Item model
                            item = purchase_order_item.item
                            item.quantity_on_hand += purchase_order_item.quantity
                            item.save()

                            # Save data in StockMovement
                            StockMovement.objects.create(
                                item=item,
                                quantity=purchase_order_item.quantity,
                                movement_type='receipt',
                                # Assuming 'supplier' is a field in your PurchaseOrderItem model
                                source_content_object=purchase_order.supplier,
                                destination=purchase_order_item.location,
                                user=self.request.user,
                                purpose=f"{self.request.user.email} received shipment of {purchase_order_item.quantity} units of {item.name} from {purchase_order.supplier}"
                            )

                            # Save data in InventoryTransaction
                            InventoryTransaction.objects.create(
                                item=item,
                                location=purchase_order_item.location,
                                transaction_type='purchase',
                                quantity=purchase_order_item.quantity,
                                user=self.request.user,
                            )

                # Save total cost in PurchaseOrder
                purchase_order.total_cost = total_cost
                purchase_order.save()

                self.response = {"message": 'Purchase created successfully!', "success": True}
                return JsonResponse(self.response)

        except Exception as e:
            self.response = {"message": str(e), "success": False}
            return JsonResponse(self.response)

        context = {
            'form': form,
        }
        return render(self.request, self.template_name, context)


class PurchaseOrderUpdateView(UpdateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'inventory_app/item/purchase/edit.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('id')
        return get_object_or_404(PurchaseOrder, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        PurchaseOrderItemFormSet = inlineformset_factory(PurchaseOrder, PurchaseOrderItem, form=PurchaseOrderItemForm,
                                                         extra=0)
        context['purchase_order_item_formset'] = PurchaseOrderItemFormSet(self.request.POST or None,
                                                                          instance=self.object)
        context['order'] = self.object  # Get id for purchase order
        context['order_id'] = self.object.order_id  # Get order id for purchase order
        return context

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data(form=form)
        purchase_order_formset = context['purchase_order_item_formset']

        try:
            if all([form.is_valid(), purchase_order_formset.is_valid()]):
                purchase_order = form.save()

                total_cost = 0
                for form in purchase_order_formset:
                    if form.is_valid():
                        purchase_order_item = form.save(commit=False)
                        purchase_order_item.purchase_order = purchase_order
                        purchase_order_item.save()

                        # Calculate total cost
                        total_cost += purchase_order_item.unit_price * purchase_order_item.quantity

                        if purchase_order.status != 'draft':
                            # Update quantity_on_hand in Item model
                            item = purchase_order_item.item
                            item.quantity_on_hand += purchase_order_item.quantity
                            item.save()

                            # Save data in StockMovement
                            StockMovement.objects.create(
                                item=item,
                                quantity=purchase_order_item.quantity,
                                movement_type='receipt',
                                source_content_object=purchase_order.supplier,
                                destination=purchase_order_item.location,
                                user=self.request.user,
                                purpose=f"{self.request.user.email} received shipment of {purchase_order_item.quantity} units of {item.name} from {purchase_order.supplier}"
                            )

                            # Save data in InventoryTransaction
                            InventoryTransaction.objects.create(
                                item=item,
                                location=purchase_order_item.location,
                                transaction_type='purchase',
                                quantity=purchase_order_item.quantity,
                                user=self.request.user,
                            )

                # Save total cost in PurchaseOrder
                purchase_order.total_cost = total_cost
                purchase_order.save()

                self.response = {"message": 'Purchase updated successfully!', "success": True}
                return JsonResponse(self.response)

            else:
                form_errors = json.dumps(form.errors)
                formset_errors = json.dumps([form.errors for form in purchase_order_formset])
                self.response = {"message": "Form validation failed", "success": False, "form_errors": form_errors,
                                 "formset_errors": formset_errors}
                return JsonResponse(self.response)

        except Exception as e:
            traceback_str = traceback.format_exc()  # Get the traceback as a string
            self.response = {"message": f"{type(e).__name__}: {str(e)}", "success": False, "traceback": traceback_str}
            return JsonResponse(self.response)

        context = {
            'form': form,
        }
        return render(self.request, self.template_name, context)


class ApprovePurchaseOrderView(View):
    def post(self, request, *args, **kwargs):
        purchase_order = get_object_or_404(PurchaseOrder, id=kwargs['id'])
        purchase_order.status = 'fulfilled'
        purchase_order.approve_order()
        purchase_order.save()
        return JsonResponse({"success": True})


class PurchaseOrderItemDataView(View):
    def get(self, request, *args, **kwargs):
        data = PurchaseOrderItem.objects.all()
        data_for_datatables = [{
            'id': item.id,
            'purchase_order': item.purchase_order.order_id,
            'item_name': item.item.name,
            'quantity': item.quantity,
            'unit_price': str(item.unit_price),
            'total_price': str(item.quantity * item.unit_price),  # Assuming unit_price field exists in your model
        } for item in data]

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': len(data_for_datatables),
            'recordsFiltered': len(data_for_datatables),
            'data': data_for_datatables,
        })


class PurchaseOrderDataView(View):
    def get(self, request, *args, **kwargs):
        data = PurchaseOrder.objects.all()
        data_for_datatables = [{
            'id': purchase_order.id,
            'order_id': purchase_order.order_id,
            'supplier': purchase_order.supplier.name,
            'total_cost': str(sum(item.quantity * item.unit_price for item in
                                  PurchaseOrderItem.objects.filter(purchase_order=purchase_order))),
            'order_date': purchase_order.order_date.strftime('%Y-%m-%d'),
            'expected_delivery_date': purchase_order.expected_delivery_date.strftime(
                '%Y-%m-%d') if purchase_order.expected_delivery_date else None,
            'status': purchase_order.get_status_display(),
            'items': [{
                'item_name': item.item.name,
                'quantity': item.quantity,
                'unit_price': str(item.unit_price),
            } for item in PurchaseOrderItem.objects.filter(purchase_order=purchase_order)]
        } for purchase_order in data]

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': len(data_for_datatables),
            'recordsFiltered': len(data_for_datatables),
            'data': data_for_datatables,
        })
