from django import forms
from django.db import models

from auth_app.models import AppUser
from hr_app.models import Department, SubDepartmentMaster, Employee
from .models import Location, Supplier, ItemCategory, ItemSubcategory, Item, Equipment, EquipmentCategory, \
    EquipmentSubcategory, PurchaseOrder, PurchaseOrderItem, ItemRequisition, ItemRequisitionItem


class SupplierForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    contact_person = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    contact_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-sm'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-sm'}))

    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'contact_number', 'email', 'address']


class LocationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select(
        attrs={'class': 'form-select form-select-sm',
               'data-control': 'select2',
               'data-allow-clear': 'true',
               'data-placeholder': 'Select Department',
               'data-dropdown-parent': '#locationModal',
               }))
    sub_department = forms.ModelChoiceField(queryset=SubDepartmentMaster.objects.all(), widget=forms.Select(
        attrs={'class': 'form-select form-select-sm',
               'data-control': 'select2',
               'data-allow-clear': 'true',
               'data-placeholder': 'Select Sub Department',
               'data-dropdown-parent': '#locationModal',
               }))

    class Meta:
        model = Location
        fields = ['name', 'capacity', 'department', 'sub_department']


class ItemCategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-sm'}))

    class Meta:
        model = ItemCategory
        fields = ['name', 'description']


class ItemSubcategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    category = forms.ModelChoiceField(queryset=ItemCategory.objects.all(), widget=forms.Select(
        attrs={'class': 'form-select form-select-sm',
               'data-control': 'select2',
               'data-allow-clear': 'true',
               'data-placeholder': 'Select Category',
               'data-dropdown-parent': '#itemSubcategoryModal',
               }))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-sm'}))

    class Meta:
        model = ItemSubcategory
        fields = ['name', 'category', 'description']


class ItemForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-sm'}),
                                  required=False)
    reorder_level = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
                                       required=False, min_value=0)
    alert_quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
                                        required=False, min_value=0)
    unit_of_measure = forms.CharField(max_length=50,
                                      widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), widget=forms.Select(
        attrs={'class': 'form-select form-select-sm',
               'data-control': 'select2',
               'data-allow-clear': 'false',
               'data-dropdown-parent': '#itemModal',
               'data-placeholder': 'Select Supplier',
               }))
    category = forms.ModelChoiceField(queryset=ItemCategory.objects.all(), widget=forms.Select(
        attrs={'class': 'form-select form-select-sm',
               'data-control': 'select2',
               'data-dropdown-parent': '#itemModal',
               'data-allow-clear': 'false',
               'data-placeholder': 'Select Category',
               }))
    subcategory = forms.ModelChoiceField(queryset=ItemSubcategory.objects.all(), widget=forms.Select(
        attrs={'class': 'form-select form-select-sm',
               'data-control': 'select2',
               'data-allow-clear': 'false',
               'data-dropdown-parent': '#itemModal',
               'data-placeholder': 'Select Subcategory',
               }))
    brand_name = forms.CharField(max_length=255,
                                 widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    dosage_form = forms.ChoiceField(choices=Item.DOSAGE_FORM_CHOICES,
                                    widget=forms.Select(attrs={'class': 'form-select form-select-sm',
                                                               'data-dropdown-parent': '#itemModal',
                                                               }))

    strength = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
                               required=False)
    requires_prescription = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                                               required=False)
    can_be_sold = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    storage_conditions = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-sm'}),
                                         required=False)
    item_type = forms.ChoiceField(choices=Item.ITEM_TYPES, widget=forms.Select(attrs={'class': 'form-select'
                                                                                               'form-select-sm',
                                                                                      'data-dropdown-parent': '#itemModal',
                                                                                      }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dosage_form'].label = "Select Dosage Form"

    class Meta:
        model = Item
        fields = ['name', 'description', 'reorder_level', 'alert_quantity', 'unit_of_measure',
                  'supplier', 'category', 'subcategory', 'dosage_form', 'strength', 'requires_prescription',
                  'can_be_sold', 'brand_name', 'storage_conditions', 'item_type']


class EquipmentCategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-sm'}))

    class Meta:
        model = EquipmentCategory
        fields = ['name', 'description']


class EquipmentSubcategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    category = forms.ModelChoiceField(queryset=EquipmentCategory.objects.all(), widget=forms.Select(
        attrs={'class': 'form-select form-select-sm',
               'data-control': 'select2',
               'data-allow-clear': 'true',
               'data-placeholder': 'Select Category',
               'data-dropdown-parent': '#equipmentSubcategoryModal',
               }))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-sm'}))

    class Meta:
        model = EquipmentSubcategory
        fields = ['name', 'category', 'description']


class EquipmentForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-sm'}),
                                  required=False)
    quantity_on_hand = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
                                          required=False, min_value=0)
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), widget=forms.Select(
        attrs={'class': 'form-select form-select-sm',
               'data-control': 'select2',
               'data-allow-clear': 'true',
               'data-placeholder': 'Select Supplier',
               }))
    category = forms.ModelChoiceField(queryset=EquipmentCategory.objects.all(), widget=forms.Select(
        attrs={'class': 'form-select form-select-sm',
               'data-control': 'select2',
               'data-allow-clear': 'true',
               'data-placeholder': 'Select Category',
               }))
    subcategory = forms.ModelChoiceField(queryset=EquipmentSubcategory.objects.all(), widget=forms.Select(
        attrs={'class': 'form-select form-select-sm',
               'data-control': 'select2',
               'data-allow-clear': 'true',
               'data-placeholder': 'Select Subcategory',
               }))
    manufacturer = forms.CharField(max_length=255,
                                   widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
                                   required=False)
    model_number = forms.CharField(max_length=255,
                                   widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
                                   required=False)
    serial_number = forms.CharField(max_length=255,
                                    widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    warranty_information = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-sm'}),
                                           required=False)
    maintenance_schedule = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-sm'}),
                                           required=False)
    usage_instructions = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-sm'}),
                                         required=False)
    status = forms.ChoiceField(choices=Equipment.STATUS_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
    additional_details = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-sm'}),
                                         required=False)

    class Meta:
        model = Equipment
        fields = ['name', 'description', 'quantity_on_hand', 'manufacturer', 'model_number', 'serial_number',
                  'warranty_information', 'maintenance_schedule', 'usage_instructions', 'status', 'additional_details']


class ItemRequisitionForm(forms.ModelForm):
    class Meta:
        model = ItemRequisition
        fields = ['requisition_type', 'location', 'supplier', 'sub_department', 'requested_by', 'description',
                  'agree_to_terms']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            if user.is_superuser:
                self.fields['sub_department'].queryset = SubDepartmentMaster.objects.all()
                # Filter AppUser objects to only include those who are staff and have a role
                self.fields['requested_by'].queryset = AppUser.objects.filter(is_staff=True,
                                                                              role__isnull=False)
            else:
                employee = Employee.objects.filter(user=user).first()
                if employee:
                    self.fields['sub_department'].queryset = SubDepartmentMaster.objects.filter(
                        id=employee.sub_department.id)
                    # Filter AppUser objects to only include those who are staff and have a role
                    self.fields['requested_by'].queryset = AppUser.objects.filter(id=user.id, is_staff=True,
                                                                                  role__isnull=False)

        # Set empty_label to None to remove the empty option
        self.fields['sub_department'].empty_label = None
        self.fields['requested_by'].empty_label = None


class ItemRequisitionItemForm(forms.ModelForm):
    class Meta:
        model = ItemRequisitionItem
        fields = ['item', 'quantity', 'approved_quantity', 'remark']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.all()
        self.fields['item'].widget.attrs.update(
            {'class': 'form-control form-select-sm item-select', 'data-placeholder': 'Select an item',
             'style': 'width: 100%;'})
        self.fields['quantity'].widget = forms.NumberInput(attrs={'class': 'form-control form-control-sm'})
        self.fields['approved_quantity'].widget = forms.NumberInput(attrs={'class': 'form-control form-control-sm'})
        self.fields['remark'].widget = forms.Textarea(attrs={'class': 'form-control form-control-sm'})


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'expected_delivery_date', 'status']


class PurchaseOrderItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = ['item', 'quantity', 'unit_price', 'expiration_date', 'location']

    def clean(self):
        cleaned_data = super().clean()
        # Check if the DELETE checkbox is checked
        if self.cleaned_data.get('DELETE'):
            # If checked, set a flag or manipulate the form data to indicate deletion
            cleaned_data['DELETE'] = True
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(PurchaseOrderItemForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['unit_price'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['expiration_date'].widget = forms.DateInput(attrs={'class': 'form-control'})
        self.fields['location'].queryset = Location.objects.all()  # Add this line
        self.fields['location'].widget.attrs.update(
            {'class': 'form-control form-select-sm location-select', 'data-placeholder': 'Select warehouse',
             'style': 'width: 100%;'})
        self.fields['item'].queryset = Item.objects.all()  # Add this line
        self.fields['item'].widget.attrs.update(
            {'class': 'form-control form-select-sm item-select', 'data-placeholder': 'Select an item',
             'style': 'width: 100%;'})
