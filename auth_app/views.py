from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password  # Import for password validation (optional)
from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from django.views.generic.edit import FormView
from django.views import View

from .constants import get_model_name  # make sure to import the function
from .forms import UserGroupCreateForm, PermissionForm, RoleForm
from .models import AppGroup, Permission, Role, AppUser, FailedLoginAttempt
from hr_app.models import Employee, EmployeePhoto


# -----------------------------------------------------------------------------------------------
# AUTHENTICATION
# ------------------------------------------------------------------------------------------------
class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'auth_app/login/signin.html'
    success_url = '/dashboard/'

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        ip_address = self.request.META.get('REMOTE_ADDR')

        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                return redirect(self.success_url)
        else:
            print("Authentication failed")  # Debugging statement
            FailedLoginAttempt.objects.create(username=email, timestamp=timezone.now(),
                                              attempt_type="Invalid Credentials", ip_address=ip_address)
            return JsonResponse({'success': False, 'error': 'Invalid credentials.'})

    def form_invalid(self, form):
        email = form.data.get('username')
        password = form.data.get('password')

        ip_address = self.request.META.get('REMOTE_ADDR')

        # Email Validation
        try:
            validate_email(email)
        except ValidationError:
            print("Email validation failed")  # Debugging statement
            FailedLoginAttempt.objects.create(username=email, timestamp=timezone.now(), attempt_type="Invalid E-mail address",
                                              ip_address=ip_address)
            return JsonResponse({'success': False, 'error': 'Enter a valid email address.'})

        # Password Complexity Validation
        try:
            validate_password(password)
        except ValidationError as e:
            print(f"Password validation error: {e}")  # Debugging statement
            FailedLoginAttempt.objects.create(username=email, timestamp=timezone.now(),
                                              attempt_type="Weak Password",
                                              ip_address=ip_address)
            return JsonResponse({'success': False, 'error': 'Password requirements not met.'})

        # This method is called when the form is invalid.
        # If the form is invalid for reasons other than email or password validation,
        # return a general error message.
        return JsonResponse({'success': False, 'error': 'Invalid credentials'})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/login/')  # Redirect to a login page


# -----------------------------------------------------------------------------------------------
# USER GROUP
# ------------------------------------------------------------------------------------------------
class UserGroupCRUDView(View):
    template_name = "auth_app/group/group_list.html"  # Adapt to your template

    def get(self, request, *args, **kwargs):
        form = UserGroupCreateForm()
        context = {
            'form': form,
            # Add any other context variables you need
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_group_id = request.POST.get('id')
        name = request.POST.get('name')
        # Add any other fields you need

        if user_group_id:
            user_group = AppGroup.objects.get(id=user_group_id)
            if AppGroup.objects.filter(name__iexact=name).exclude(id=user_group_id).exists():
                self.response = {"message": 'AppGroup with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = UserGroupCreateForm(request.POST, instance=user_group)
                success_message = 'AppGroup updated successfully!'
        else:
            if AppGroup.objects.filter(name__iexact=name).exists():
                self.response = {"message": 'AppGroup with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = UserGroupCreateForm(request.POST)
                success_message = 'AppGroup created successfully!'

        if form.is_valid():
            form.save()
            self.response = {"message": success_message, "success": True}
            return JsonResponse(self.response)

        context = {
            'form': form,
            # Add any other context variables you need
        }
        return render(request, self.template_name, context)


class UserGroupDataView(View):
    def get(self, request, *args, **kwargs):
        # Query all data
        data = AppGroup.objects.all()

        STATUS_CHOICES_DICT = {
            'active': '<span class="badge bg-soft-success p-1 text-success">Active</span>',
            'inactive': '<span class="badge bg-soft-warning p-1 text-warning">Inactive</span>',
            'locked': '<span class="badge bg-soft-danger p-1 text-danger">Locked</span>',
        }

        # STATUS_CHOICES_DICT = {
        #     'active': '<div class="text-success">Active</div>',
        #     'inactive': '<div class="text-warning">Inactive</div>',
        #     'locked': '<div class="text-danger">Locked</div>',
        # }

        # Format the data for DataTables
        data_for_datatables = [{
            'id': usergroup.id,
            'name': usergroup.name,
            'parent': usergroup.parent.name if usergroup.parent else None,  # Use the parent's name
            'parent_id': usergroup.parent.id if usergroup.parent else None,  # Use the parent's ID
            'description': usergroup.description,
            'status': usergroup.status,
            'status_display': STATUS_CHOICES_DICT.get(usergroup.status,
                                                      '<span class="badge badge-secondary">Unknown</span>'),
        } for usergroup in data]

        # Return the data
        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),  # The draw counter for DataTables
            'recordsTotal': len(data_for_datatables),  # The total number of records
            'recordsFiltered': len(data_for_datatables),  # The number of records after filtering
            'data': data_for_datatables,  # The data to display
        })


class UserGroupDeleteView(View):
    def post(self, request, *args, **kwargs):
        # Get the IDs from the request
        ids = request.POST.getlist('ids[]')

        # Delete the AppGroup objects with the given IDs
        AppGroup.objects.filter(id__in=ids).delete()

        # Return a success response with a message
        return JsonResponse({
            'success': True,
            'message': 'Selection have been successfully deleted!'
        })


# -----------------------------------------------------------------------------------------------
# END USER GROUP
# ------------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------
# PERMISSIONS
# ------------------------------------------------------------------------------------------------

class PermissionCRUDView(View):
    template_name = "auth_app/permission/permission_list.html"  # Adapt to your template

    def get(self, request, *args, **kwargs):
        form = PermissionForm()
        context = {
            'form': form,
            # Add any other context variables you need
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        permission_id = request.POST.get('id')
        name = request.POST.get('name')
        # Add any other fields you need

        if permission_id:
            permission = Permission.objects.get(id=permission_id)
            if Permission.objects.filter(name__iexact=name).exclude(id=permission_id).exists():
                self.response = {"message": 'Permission with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = PermissionForm(request.POST, instance=permission)
                success_message = 'Permission updated successfully!'
        else:
            if Permission.objects.filter(name__iexact=name).exists():
                self.response = {"message": 'Permission with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = PermissionForm(request.POST)
                success_message = 'Permission created successfully!'

        if form.is_valid():
            form.save()
            self.response = {"message": success_message, "success": True}
            return JsonResponse(self.response)

        context = {
            'form': form,
            # Add any other context variables you need
        }
        return render(request, self.template_name, context)


class PermissionDataView(View):
    def get(self, request, *args, **kwargs):
        # Query all data and prefetch related permissions
        content_types = ContentType.objects.exclude(
            app_label__in=['auth', 'contenttypes', 'sessions', 'admin', 'guardian']
        ).prefetch_related(
            Prefetch(
                'auth_app_permissions',
                queryset=Permission.objects.all(),
                to_attr='fetched_permissions'
            )
        )

        # Format the data for DataTables
        data_for_datatables = [{
            'id': content_type.id,
            'module': get_model_name(content_type.app_label, content_type.model),
            'permissions': [perm.name for perm in content_type.fetched_permissions],
        } for content_type in content_types]

        # Return the data
        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),  # The draw counter for DataTables
            'recordsTotal': len(data_for_datatables),  # The total number of records
            'recordsFiltered': len(data_for_datatables),  # The number of records after filtering
            'data': data_for_datatables,  # The data to display
        })


# -----------------------------------------------------------------------------------------------
# PERMISSIONS
# ------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
# ROLES
# ------------------------------------------------------------------------------------------------
class RoleCRUDView(View):
    template_name = 'auth_app/role/role_list.html'

    def get(self, request, *args, **kwargs):
        form = RoleForm()
        roles = Role.objects.all()

        # Calculate total users for each role and retrieve full names and images
        for role in roles:
            users = AppUser.objects.filter(role=role)
            role.total_users = users.count()
            role.users = [{'full_name': user.employee.full_name, 'image_url': EmployeePhoto.objects.filter(
                employee=user.employee).first().image.url if EmployeePhoto.objects.filter(
                employee=user.employee).exists() else None} for user in users]

        content_types = ContentType.objects.exclude(
            app_label__in=['auth', 'contenttypes', 'sessions', 'admin', 'guardian', ]
        )
        module_names = {ct: get_model_name(ct.app_label, ct.model) for ct in content_types}
        context = {
            'form': form,
            'roles': roles,
            'content_types': module_names,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        role_id = request.POST.get('id')
        name = request.POST.get('name')
        # Add any other fields you need

        if role_id:
            role = Role.objects.get(id=role_id)
            if Role.objects.filter(name__iexact=name).exclude(id=role_id).exists():
                self.response = {"message": 'Role with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = RoleForm(request.POST, instance=role)
                success_message = 'Role updated successfully!'
        else:
            if Role.objects.filter(name__iexact=name).exists():
                self.response = {"message": 'Role with this Name already exists.'}
                return JsonResponse(self.response)
            else:
                form = RoleForm(request.POST)
                success_message = 'Role created successfully!'

        if form.is_valid():
            form.save()
            self.response = {"message": success_message, "success": True}
            return JsonResponse(self.response)

        context = {
            'form': form,
            # Add any other context variables you need
        }
        return render(request, self.template_name, context)


# CLASS FOR AJAX TABLE FOR ROLES
class RoleDataView(View):
    def get(self, request, *args, **kwargs):
        # Query all data
        data = Role.objects.all()

        # Format the data for DataTables
        data_for_datatables = [{
            'id': role.id,
            'name': role.name,
            'description': role.description,
        } for role in data]

        # Return the data
        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),  # The draw counter for DataTables
            'recordsTotal': len(data_for_datatables),  # The total number of records
            'recordsFiltered': len(data_for_datatables),  # The number of records after filtering
            'data': data_for_datatables,  # The data to display
        })


# CLASS FOR AJAX CARD FOR ROLES
class RoleCardView(View):
    def get(self, request, *args, **kwargs):
        try:
            roles = Role.objects.all()
            role_list = [{'id': role.id, 'name': role.name, 'description': role.description,
                          'total_users': AppUser.objects.filter(role=role).count(),
                          'users': [{'name': user.full_name, 'image_url': EmployeePhoto.objects.filter(
                              employee=user.employee).first().image.url if EmployeePhoto.objects.filter(
                              employee=user.employee).exists() else None} for user in
                                    AppUser.objects.filter(role=role)],
                          'permissions': [{'id': permission.id, 'name': permission.name,
                                           'content_type': permission.content_type.name} for permission in
                                          role.permissions.all()]} for role in roles]
            return JsonResponse(role_list, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Role does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# CLASS FOR VIEW SINGLE ROLE WITH PERMISSIONS
class RoleDetailView(View):
    template_name = 'auth_app/role/role_detail.html'

    def get(self, request, *args, **kwargs):
        form = RoleForm()
        role_id = kwargs['id']  # get the ID from the URL
        role = get_object_or_404(Role, id=role_id)  # get the Role object

        # Get all users that belong to this role
        users = AppUser.objects.filter(role=role)

        # Get the EmployeePhoto for each user
        users_with_photos = []
        for user in users:
            employee = Employee.objects.get(user=user)
            employee_photo = EmployeePhoto.objects.filter(employee=employee).first()
            if employee_photo:
                users_with_photos.append((user, employee_photo.image.url))
            else:
                users_with_photos.append((user, None))

        content_types = ContentType.objects.exclude(
            app_label__in=['auth', 'contenttypes', 'sessions', 'admin', 'guardian', ]
        )
        module_names = {ct: get_model_name(ct.app_label, ct.model) for ct in content_types}
        context = {
            'form': form,
            'role': role,
            'users_with_photos': users_with_photos,  # Add users with photos to the context
            'content_types': module_names,
        }
        return render(request, self.template_name, context)
