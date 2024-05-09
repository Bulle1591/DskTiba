# forms.py
from django import forms
from .models import (
    DepartmentType, Department,
    SubDepartmentMaster, Designation,
    JobType, Employee, EmployeeDocument,
    EmployeePhoto, EmployeeContact
)
from auth_app.models import AppUser, Role


class DepartmentTypeForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES,
                               label="Select Status",
                               widget=forms.Select(attrs={'class': 'form-select form-select-sm',
                                                          'data-control': 'select2',
                                                          'data-allow-clear': 'true',
                                                          'data-dropdown-parent': '#departmentTypeModal',
                                                          'data-placeholder': 'Select Status',
                                                          }))

    class Meta:
        model = DepartmentType
        fields = ['id', 'name', 'code', 'status']


class DesignationForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES,
                               label="Select Status",
                               widget=forms.Select(attrs={'class': 'form-select form-select-sm',
                                                          'data-control': 'select2',
                                                          'data-allow-clear': 'true',
                                                          'data-dropdown-parent': '#designationModal',
                                                          'data-placeholder': 'Select Status',
                                                          }))

    class Meta:
        model = Designation
        fields = ['id', 'title', 'description', 'status']


class JobTypeForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES,
                               label="Select Status",
                               widget=forms.Select(attrs={'class': 'form-select form-select-sm',
                                                          'data-control': 'select2',
                                                          'data-allow-clear': 'true',
                                                          'data-dropdown-parent': '#jobTypeModal',
                                                          'data-placeholder': 'Select Status',
                                                          }))

    class Meta:
        model = JobType
        fields = ['id', 'title', 'description', 'status']


class DepartmentForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES,
                               label="Select Status",
                               widget=forms.Select(attrs={'class': 'form-select form-select-sm',
                                                          'data-control': 'select2',
                                                          'data-allow-clear': 'true',
                                                          'data-placeholder': 'Select Status',
                                                          }))
    consultation = forms.BooleanField(required=False)
    discharge_approval = forms.BooleanField(required=False)

    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'status', 'consultation', 'discharge_approval']


class SubDepartmentMasterForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select(
        attrs={'class': 'form-select form-select-sm',
               'data-control': 'select2',
               'data-allow-clear': 'true',
               'data-placeholder': 'Select Department',
               'data-dropdown-parent': '#subDepartmentModal',
               }))
    department_types = forms.ModelMultipleChoiceField(queryset=DepartmentType.objects.all(),
                                                      widget=forms.SelectMultiple(
                                                          attrs={'class': 'form-select form-select-sm',
                                                                 'data-control': 'select2',
                                                                 'data-allow-clear': 'true',
                                                                 'data-placeholder': 'Select Department Types',
                                                                 'multiple': 'multiple',
                                                                 'data-dropdown-parent': '#subDepartmentModal',
                                                                 }))
    status = forms.ChoiceField(choices=STATUS_CHOICES,
                               label="Select Status",
                               widget=forms.Select(attrs={'class': 'form-select form-select-sm',
                                                          'data-control': 'select2',
                                                          'data-allow-clear': 'true',
                                                          'data-dropdown-parent': '#subDepartmentModal',
                                                          'data-placeholder': 'Select Status',
                                                          }))

    class Meta:
        model = SubDepartmentMaster
        fields = ['name', 'department', 'department_types', 'status']


class AppUserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_active = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    is_staff = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    role = forms.ModelChoiceField(queryset=Role.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-select form-select-sm',
                                                             'data-control': 'select2',
                                                             'data-allow-clear': 'false',
                                                             'data-dropdown-parent': '#addEmployeeModal',
                                                             }))

    class Meta:
        model = AppUser
        fields = ['email', 'password', 'first_name', 'last_name', 'is_active', 'is_staff', 'role']


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['user', 'status']

    emp_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    national_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    qualification = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    licence_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    designation = forms.ModelChoiceField(
        queryset=Designation.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select form-select-sm',
                                   'data-control': 'select2',
                                   'data-allow-clear': 'false',
                                   'data-dropdown-parent': '#addEmployeeModal',
                                   }))
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'dd/mm/yyyy'
            }
        )
    )
    date_joined = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'dd/mm/yyyy'
            }
        )
    )

    job_type = forms.ModelChoiceField(
        queryset=JobType.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select form-select-sm',
                                   'data-control': 'select2',
                                   'data-allow-clear': 'false',
                                   'data-dropdown-parent': '#addEmployeeModal',
                                   }))
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select form-select-sm',
                                   'data-control': 'select2',
                                   'data-allow-clear': 'false',
                                   'data-dropdown-parent': '#addEmployeeModal',
                                   }))
    sub_department = forms.ModelChoiceField(
        queryset=SubDepartmentMaster.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select form-select-sm',
                                   'data-control': 'select2',
                                   'data-allow-clear': 'false',
                                   'data-dropdown-parent': '#addEmployeeModal',
                                   }))
    salutation = forms.ChoiceField(
        choices=Employee.SALUTATIONS,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm',
                                   'data-control': 'select2',
                                   'data-allow-clear': 'false',
                                   'data-dropdown-parent': '#addEmployeeModal',
                                   }))

    gender = forms.ChoiceField(
        choices=Employee.GENDERS,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm',
                                   'data-control': 'select2',
                                   'data-allow-clear': 'false',
                                   'data-dropdown-parent': '#addEmployeeModal',
                                   'data-placeholder': 'Select Gender',
                                   }))

    # status = forms.ChoiceField(
    #     choices=Employee.STATUS_CHOICES,
    #     widget=forms.Select(attrs={'class': 'form-select form-select-sm',
    #                                'data-control': 'select2',
    #                                'data-allow-clear': 'false',
    #                                'data-dropdown-parent': '#addEmployeeModal',
    #                                'data-placeholder': 'Select Status',
    #                                }))


# Similarly, create forms for EmployeeContact, EmployeeDocument, and EmployeePhoto
class EmployeeContactForm(forms.ModelForm):
    class Meta:
        model = EmployeeContact
        exclude = ['employee']  # Exclude the 'employee' field

    # Customize the rendering of specific fields
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'rows': '1'
                                                           }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # Add other fields as needed


class EmployeeDocumentForm(forms.ModelForm):
    class Meta:
        model = EmployeeDocument
        exclude = ['employee']  # Exclude the 'employee' fieldfields = '__all__'

    # Customize the rendering of specific fields
    document_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    # Add other fields as needed


class EmployeePhotoForm(forms.ModelForm):
    class Meta:
        model = EmployeePhoto
        exclude = ['employee']  # Exclude the 'employee' field

    # Customize the rendering of specific fields
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    # Add other fields as needed
