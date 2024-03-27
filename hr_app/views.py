from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from django.forms import formset_factory

from auth_app.models import AppUser
from .models import (
    DepartmentType, Designation, Department,
    SubDepartmentMaster, JobType, Employee,
    EmployeeDocument, EmployeePhoto, EmployeeContact
)
from .forms import (
    DepartmentTypeForm, DesignationForm, DepartmentForm,
    SubDepartmentMasterForm, JobTypeForm, EmployeeContactForm,
    EmployeePhotoForm, EmployeeDocumentForm, EmployeeForm, AppUserForm
)

STATUS_CHOICES_DICT = {
    'active': '<span class="badge bg-info">Active</span>',
    'inactive': '<span class="badge bg-secondary">Inactive</span>',
}


# ///////////////////////////////////////////////////////
# ////////// DESIGNATION
class DesignationCRUDView(View):
    template_name = "hr_app/designation/list.html"

    def get(self, request, *args, **kwargs):
        form = DesignationForm()
        context = {
            'form': form,
            # Add any other context variables you need
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        designation_id = request.POST.get('id')
        title = request.POST.get('title')
        # Add any other fields you need

        if designation_id:
            designation = Designation.objects.get(id=designation_id)
            if Designation.objects.filter(title__iexact=title).exclude(id=designation_id).exists():
                self.response = {"message": 'Designation with this Title already exists.'}
                return JsonResponse(self.response)
            else:
                form = DesignationForm(request.POST, instance=designation)
                success_message = 'Designation updated successfully!'
        else:
            if Designation.objects.filter(title__iexact=title).exists():
                self.response = {"message": 'Designation with this Title already exists.'}
                return JsonResponse(self.response)
            else:
                form = DesignationForm(request.POST)
                success_message = 'Designation created successfully!'

        if form.is_valid():
            form.save()
            self.response = {"message": success_message, "success": True}
            return JsonResponse(self.response)

        context = {
            'form': form,
            # Add any other context variables you need
        }
        return render(request, self.template_name, context)


# CLASS FOR AJAX TABLE FOR DEPARTMENT TYPE
class DesignationDataView(View):
    def get(self, request, *args, **kwargs):
        # Query all data
        data = Designation.objects.all()

        # Format the data for DataTables
        data_for_datatables = [{
            'id': designation.id,
            'title': designation.title,
            'description': designation.description,
            'status': designation.status,
            'status_display': STATUS_CHOICES_DICT.get(designation.status,
                                                      '<span class="badge badge-secondary">Unknown</span>'),
        } for designation in data]

        # Return the data
        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),  # The draw counter for DataTables
            'recordsTotal': len(data_for_datatables),  # The total number of records
            'recordsFiltered': len(data_for_datatables),  # The number of records after filtering
            'data': data_for_datatables,  # The data to display
        })


class DesignationDeleteView(View):
    def post(self, request, *args, **kwargs):
        # Get the IDs from the request
        ids = request.POST.getlist('ids[]')

        # Delete the AppGroup objects with the given IDs
        Designation.objects.filter(id__in=ids).delete()

        # Return a success response with a message
        return JsonResponse({
            'success': True,
            'message': 'Selection have been successfully deleted!'
        })


# ///////////////////////////////////////////////////////
# ////////// JOB TYPE
class JobTypeCRUDView(View):
    template_name = "hr_app/job_type/list.html"

    def get(self, request, *args, **kwargs):
        form = JobTypeForm()
        context = {
            'form': form,
            # Add any other context variables you need
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        job_type_id = request.POST.get('id')
        title = request.POST.get('title')
        # Add any other fields you need

        if job_type_id:
            job_type = JobType.objects.get(id=job_type_id)
            if JobType.objects.filter(title__iexact=title).exclude(id=job_type_id).exists():
                self.response = {"message": 'Employment Type with this Title already exists.'}
                return JsonResponse(self.response)
            else:
                form = JobTypeForm(request.POST, instance=job_type)
                success_message = 'Employment Type updated successfully!'
        else:
            if JobType.objects.filter(title__iexact=title).exists():
                self.response = {"message": 'Employment Type with this Title already exists.'}
                return JsonResponse(self.response)
            else:
                form = JobTypeForm(request.POST)
                success_message = 'Employment Type created successfully!'

        if form.is_valid():
            form.save()
            self.response = {"message": success_message, "success": True}
            return JsonResponse(self.response)

        context = {
            'form': form,
            # Add any other context variables you need
        }
        return render(request, self.template_name, context)


# CLASS FOR AJAX TABLE FOR DEPARTMENT TYPE
class JobTypeDataView(View):
    def get(self, request, *args, **kwargs):
        # Query all data
        data = JobType.objects.all()

        # Format the data for DataTables
        data_for_datatables = [{
            'id': job_type.id,
            'title': job_type.title,
            'description': job_type.description,
            'status': job_type.status,
            'status_display': STATUS_CHOICES_DICT.get(job_type.status,
                                                      '<span class="badge badge-secondary">Unknown</span>'),
        } for job_type in data]

        # Return the data
        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),  # The draw counter for DataTables
            'recordsTotal': len(data_for_datatables),  # The total number of records
            'recordsFiltered': len(data_for_datatables),  # The number of records after filtering
            'data': data_for_datatables,  # The data to display
        })


class JobTypeDeleteView(View):
    def post(self, request, *args, **kwargs):
        # Get the IDs from the request
        ids = request.POST.getlist('ids[]')

        # Delete the AppGroup objects with the given IDs
        JobType.objects.filter(id__in=ids).delete()

        # Return a success response with a message
        return JsonResponse({
            'success': True,
            'message': 'Selection have been successfully deleted!'
        })


# ///////////////////////////////////////////////////////
# ////////// DEPARTMENT TYPE
class DepartmentTypeCRUDView(View):
    template_name = "hr_app/department_type/list.html"

    def get(self, request, *args, **kwargs):
        form = DepartmentTypeForm()
        context = {
            'form': form,
            # Add any other context variables you need
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        department_type_id = request.POST.get('id')
        name = request.POST.get('name')
        # Add any other fields you need

        if department_type_id:
            department_type = DepartmentType.objects.get(id=department_type_id)
            if DepartmentType.objects.filter(name__iexact=name).exclude(id=department_type_id).exists():
                self.response = {"message": 'DepartmentType with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = DepartmentTypeForm(request.POST, instance=department_type)
                success_message = 'DepartmentType updated successfully!'
        else:
            if DepartmentType.objects.filter(name__iexact=name).exists():
                self.response = {"message": 'DepartmentType with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = DepartmentTypeForm(request.POST)
                success_message = 'DepartmentType created successfully!'

        if form.is_valid():
            form.save()
            self.response = {"message": success_message, "success": True}
            return JsonResponse(self.response)

        context = {
            'form': form,
            # Add any other context variables you need
        }
        return render(request, self.template_name, context)


# CLASS FOR AJAX TABLE FOR DEPARTMENT TYPE
class DepartmentTypeDataView(View):
    def get(self, request, *args, **kwargs):
        # Query all data
        data = DepartmentType.objects.all()

        # Format the data for DataTables
        data_for_datatables = [{
            'id': department_type.id,
            'name': department_type.name,
            'code': department_type.code,
            'status': department_type.status,
            'status_display': STATUS_CHOICES_DICT.get(department_type.status,
                                                      '<span class="badge badge-secondary">Unknown</span>'),
        } for department_type in data]

        # Return the data
        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),  # The draw counter for DataTables
            'recordsTotal': len(data_for_datatables),  # The total number of records
            'recordsFiltered': len(data_for_datatables),  # The number of records after filtering
            'data': data_for_datatables,  # The data to display
        })


class DepartmentTypeDeleteView(View):
    def post(self, request, *args, **kwargs):
        # Get the IDs from the request
        ids = request.POST.getlist('ids[]')

        # Delete the AppGroup objects with the given IDs
        DepartmentType.objects.filter(id__in=ids).delete()

        # Return a success response with a message
        return JsonResponse({
            'success': True,
            'message': 'Selection have been successfully deleted!'
        })


# ///////////////////////////////////////////////////////
# ////////// DEPARTMENT TYPE
class DepartmentCRUDView(View):
    template_name = "hr_app/department/list.html"

    def get(self, request, *args, **kwargs):
        form = DepartmentForm()
        context = {
            'form': form,
            # Add any other context variables you need
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        department_id = request.POST.get('id')
        name = request.POST.get('name')
        # Add any other fields you need

        if department_id:
            department = Department.objects.get(id=department_id)
            if Department.objects.filter(name__iexact=name).exclude(id=department_id).exists():
                self.response = {"message": 'Department with this name already exists.'}
                return JsonResponse(self.response)
            else:
                form = DepartmentForm(request.POST, instance=department)
                success_message = 'Department updated successfully!'
        else:
            if Department.objects.filter(name__iexact=name).exists():
                self.response = {"message": 'Department with this name already exists.'}
                return JsonResponse(self.response)
            else:
                form = DepartmentForm(request.POST)
                success_message = 'Department created successfully!'

        if form.is_valid():
            form.save()
            self.response = {"message": success_message, "success": True}
            return JsonResponse(self.response)

        context = {
            'form': form,
            # Add any other context variables you need
        }
        return render(request, self.template_name, context)


# CLASS FOR AJAX TABLE FOR DEPARTMENT TYPE
class DepartmentDataView(View):
    def get(self, request, *args, **kwargs):
        # Query all data
        data = Department.objects.all()

        # Format the data for DataTables
        data_for_datatables = [{
            'id': department.id,
            'name': department.name,
            'code': department.code,
            'status': department.status,
            'consultation': department.consultation,
            'discharge_approval': department.discharge_approval,
            'status_display': STATUS_CHOICES_DICT.get(department.status,
                                                      '<span class="badge badge-secondary">Unknown</span>'),
        } for department in data]

        # Return the data
        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),  # The draw counter for DataTables
            'recordsTotal': len(data_for_datatables),  # The total number of records
            'recordsFiltered': len(data_for_datatables),  # The number of records after filtering
            'data': data_for_datatables,  # The data to display
        })


class DepartmentDeleteView(View):
    def post(self, request, *args, **kwargs):
        # Get the IDs from the request
        ids = request.POST.getlist('ids[]')

        # Delete the AppGroup objects with the given IDs
        Department.objects.filter(id__in=ids).delete()

        # Return a success response with a message
        return JsonResponse({
            'success': True,
            'message': 'Selection have been successfully deleted!'
        })


# ///////////////////////////////////////////////////////
# ////////// SUB DEPARTMENT
class SubDepartmentCRUDView(View):
    template_name = "hr_app/sub-department/list.html"

    def get(self, request, *args, **kwargs):
        form = SubDepartmentMasterForm()
        context = {
            'form': form,
            # Add any other context variables you need
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        subdepartment_id = request.POST.get('id')
        name = request.POST.get('name')
        department = request.POST.get('department')
        department_type = request.POST.get('department_type')
        status = request.POST.get('status')

        if subdepartment_id:
            subdepartment = SubDepartmentMaster.objects.get(id=subdepartment_id)
            if SubDepartmentMaster.objects.filter(name__iexact=name).exclude(id=subdepartment_id).exists():
                self.response = {"message": 'SubDepartment with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = SubDepartmentMasterForm(request.POST, instance=subdepartment)
                success_message = 'SubDepartment updated successfully!'
        else:
            if SubDepartmentMaster.objects.filter(name__iexact=name).exists():
                self.response = {"message": 'SubDepartment with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = SubDepartmentMasterForm(request.POST)
                success_message = 'SubDepartment created successfully!'

        if form.is_valid():
            form.save()
            self.response = {"message": success_message, "success": True}
            return JsonResponse(self.response)

        context = {
            'form': form,
            # Add any other context variables you need
        }
        return render(request, self.template_name, context)


class SubDepartmentDataView(View):
    def get(self, request, *args, **kwargs):
        # Query all data
        data = SubDepartmentMaster.objects.all()

        # Format the data for DataTables
        data_for_datatables = [{
            'id': subdepartment.id,
            'name': subdepartment.name,
            'department': subdepartment.department.name,
            'department_types': ', '.join([dt.name for dt in subdepartment.department_types.all()]),
            'status': subdepartment.status,
            'status_display': STATUS_CHOICES_DICT.get(subdepartment.status,
                                                      '<span class="badge badge-secondary">Unknown</span>'),
        } for subdepartment in data]

        # Return the data
        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),  # The draw counter for DataTables
            'recordsTotal': len(data_for_datatables),  # The total number of records
            'recordsFiltered': len(data_for_datatables),  # The number of records after filtering
            'data': data_for_datatables,  # The data to display
        })


# ///////////////////////////////////////////////////////
# ////////// EMPLOYEE

# GENERATE EMP NUMBER
class GenerateEmpNumberView(View):
    def get(self, request, *args, **kwargs):
        # Get the current year
        current_year = timezone.now().year

        # Count the number of AppUser except one with no employee instance objects and add 1
        next_number = AppUser.objects.exclude(employee__isnull=True).count() + 1

        # Format the next_number with leading zeros
        formatted_number = str(next_number).zfill(3)  # Change 3 to the number of digits you want

        # Generate the next emp_number
        next_emp_number = "EMP" + formatted_number + str(current_year)

        return JsonResponse({'emp_number': next_emp_number})


# class EmployeeCreateView(View):
#     template_name = 'hr_app/employee/list.html'

#     def get(self, request):
#         # Create a formset class
#         DocumentFormSet = formset_factory(EmployeeDocumentForm, extra=1)

#         user_form = AppUserForm()
#         employee_form = EmployeeForm()
#         contact_form = EmployeeContactForm()
#         document_formset = DocumentFormSet(prefix='documents')  # Initialize the formset
#         photo_form = EmployeePhotoForm()
#         context = {
#             'user_form': user_form,
#             'employee_form': employee_form,
#             'contact_form': contact_form,
#             'document_formset': document_formset,  # Include the formset in the context
#             'photo_form': photo_form,
#         }
#         return render(request, self.template_name, context)


# CREATE EMPLOYEE
class EmployeeCreateView(View):
    template_name = 'hr_app/employee/list.html'
    
    def get(self, request):
        user_form = AppUserForm()
        employee_form = EmployeeForm()
        contact_form = EmployeeContactForm()
        DocumentFormSet = formset_factory(EmployeeDocumentForm, extra=1)
        document_formset = DocumentFormSet(prefix='documents')
        photo_form = EmployeePhotoForm()

        context = {
            'user_form': user_form,
            'employee_form': employee_form,
            'contact_form': contact_form,
            'document_formset': document_formset,
            'photo_form': photo_form,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        DocumentFormSet = formset_factory(EmployeeDocumentForm, extra=1)

        user_form = AppUserForm(request.POST)
        employee_form = EmployeeForm(request.POST)
        contact_form = EmployeeContactForm(request.POST)
        document_formset = DocumentFormSet(request.POST, request.FILES, prefix='documents')
        photo_form = EmployeePhotoForm(request.POST, request.FILES)

        if all([user_form.is_valid(), employee_form.is_valid(), contact_form.is_valid(), document_formset.is_valid(), photo_form.is_valid()]):
            email = user_form.cleaned_data.get('email')
            phone_number = contact_form.cleaned_data.get('phone_number')

            if AppUser.objects.filter(email=email).exists():
                return JsonResponse({"message": "A user with this email already exists.", "success": False})
            if EmployeeContact.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({"message": "A contact with this phone number already exists.", "success": False})

            user_instance = user_form.save()
            employee_instance = employee_form.save(commit=False)
            employee_instance.user = user_instance
            employee_instance.save()
            contact_instance = contact_form.save(commit=False)
            contact_instance.employee = employee_instance
            contact_instance.save()
            for form in document_formset:
                document_instance = form.save(commit=False)
                document_instance.employee = employee_instance
                document_instance.save()
            photo_instance = photo_form.save(commit=False)
            photo_instance.employee = employee_instance
            photo_instance.save()
            return JsonResponse({"message": "Employee created successfully.", "success": True})
        else:
            error_messages = []
            for form in [user_form, employee_form, contact_form, photo_form]:
                for field, errors in form.errors.items():
                    error_messages.append(f"{field.capitalize()}: {', '.join(errors)}")
            return JsonResponse({"message": "\n".join(error_messages), "success": False})




# FETCH EMPLOYEE DATA TO BE DISPLAYED IN THE EMPLOYEE CARD
class EmployeeCardView(View):
    def get(self, request, *args, **kwargs):
        # Query all data
        data = Employee.objects.select_related('user', 'designation', 'job_type', 'department').prefetch_related(
            'employeecontact', 'employeedocument', 'employeephoto').all()

        # Format the data for DataTables
        data_for_datatables = [{
            'id': employee.user.id,
            'email': employee.user.email,
            'employee_id': employee.id,
            'emp_number': employee.emp_number,
            'qualification': employee.qualification,
            'status': employee.status,
            'first_name': employee.user.first_name,
            'last_name': employee.user.last_name,
            'designation': employee.designation.title if employee.designation else None,
            'job_type': employee.job_type.title if employee.job_type else None,
            'department': employee.department.name if employee.department else None,
            'contact': [{
                'phone': contact.phone_number,
                'address': contact.address,
            } for contact in employee.employeecontact.all()],
            'document': [{
                'document_type': document.document_type,
                'document_file': document.file.url,
            } for document in employee.employeedocument.all()],
            'photo': [{
                'photo_file': photo.image.url,
            } for photo in employee.employeephoto.all()],
        } for employee in data]

        # Return the data
        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),  # The draw counter for DataTables
            'recordsTotal': len(data_for_datatables),  # The total number of records
            'recordsFiltered': len(data_for_datatables),  # The number of records after filtering
            'data': data_for_datatables,  # The data to display
        })
