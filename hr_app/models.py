from django.db import models
from auth_app.models import AppUser


class Designation(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'status': self.status,
        }


class JobType(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'status': self.status,
        }


class DepartmentType(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    consultation = models.BooleanField(default=False)
    discharge_approval = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'department': self.name,
            'code': self.code,
            'status': self.status,
            'consultation': self.consultation,
            'discharge_approval_required': self.discharge_approval,
        }


class SubDepartmentMaster(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    department_types = models.ManyToManyField(DepartmentType)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Now, when you upload a file, it will be saved in a directory named employee_<emp_number> where <emp_number> is the
# emp_number of the Employee instance. def user_directory_path(instance, filename): # file will be uploaded to
# MEDIA_ROOT / employee_<id>/<filename> return 'employee_{0}/{1}'.format(instance.employee.emp_number, filename)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/staff/files/<employee_id>/<filename>
    return 'staff/files/{0}/{1}'.format(instance.employee.id, filename)


class Employee(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        # Add more choices as needed
    ]
    GENDERS = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDERS,
        default='N',
    )
    SALUTATIONS = [
        ('Mr', 'Mr'),
        ('Ms', 'Ms'),
        ('Dr', 'Dr'),
        # add more salutations as needed
    ]
    salutation = models.CharField(
        max_length=2,
        choices=SALUTATIONS,
        default='Mr',
    )
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    emp_number = models.CharField(max_length=100, blank=True, unique=True, null=True)
    qualification = models.CharField(max_length=255)
    licence_number = models.CharField(max_length=100)
    national_id = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    date_joined = models.DateField()
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True)
    job_type = models.ForeignKey(JobType, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    sub_department = models.ForeignKey(SubDepartmentMaster, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"Profile of {self.user}"

    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


class EmployeeContact(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employeecontact')
    address = models.TextField()
    phone_number = models.CharField(max_length=15)


class EmployeeDocument(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employeedocument')
    document_type = models.CharField(max_length=255)
    file = models.FileField(upload_to=user_directory_path)


class EmployeePhoto(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employeephoto')
    image = models.ImageField(upload_to=user_directory_path, default='media/staff/avatar.jpg')
