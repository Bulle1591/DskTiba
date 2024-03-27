from django.contrib import admin
from .models import (DepartmentType, Department, SubDepartmentMaster, Employee, EmployeeContact, EmployeeDocument,
                     EmployeePhoto
                     )


@admin.register(DepartmentType)
class DepartmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status')


@admin.register(Department)
class DepartmentMasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'consultation', 'discharge_approval')


@admin.register(SubDepartmentMaster)
class SubDepartmentMasterAdmin(admin.ModelAdmin):
    list_display = ('department', 'name', 'status')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'emp_number', 'qualification', 'licence_number', 'date_of_birth', 'date_joined',
                    'designation', 'job_type', 'department', 'status']
    search_fields = ['user__username', 'emp_number', 'qualification', 'licence_number']
    list_filter = ['status', 'designation', 'job_type', 'department']


admin.site.register(Employee, EmployeeAdmin)


class EmployeeContactAdmin(admin.ModelAdmin):
    list_display = ['employee', 'address', 'phone_number']
    search_fields = ['employee__user__username', 'address', 'phone_number']


admin.site.register(EmployeeContact, EmployeeContactAdmin)


class EmployeeDocumentAdmin(admin.ModelAdmin):
    list_display = ['employee', 'document_type']
    search_fields = ['employee__user__username', 'document_type']


admin.site.register(EmployeeDocument, EmployeeDocumentAdmin)


class EmployeePhotoAdmin(admin.ModelAdmin):
    list_display = ['employee', 'image']
    search_fields = ['employee__user__username']


admin.site.register(EmployeePhoto, EmployeePhotoAdmin)
