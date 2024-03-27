from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(email, password, **extra_fields)

        # Create a group named "Superuser" if it doesn't exist
        group, created = Group.objects.get_or_create(name='Superuser')

        # Add the user to the "Superuser" group
        user.groups.add(group)

        return user


class AppGroup(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('locked', 'Locked'),
    ], default='active')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'


class Permission(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='auth_app_permissions',
                                     null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'


class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    # Add a ManyToManyField to link permissions directly
    permissions = models.ManyToManyField(Permission)

    def user_count(self):
        return self.user_set.count()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'


class GroupPermission(models.Model):
    group = models.ForeignKey(AppGroup, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        permission_names = ", ".join([str(p.name) for p in self.permissions.all()])
        return f"{self.group.name} - {permission_names}"

    class Meta:
        verbose_name = 'Group Permission'
        verbose_name_plural = 'Group Permissions'


class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class AppUserGroup(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    group = models.ForeignKey(AppGroup, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'group')
        verbose_name = 'User Group'
        verbose_name_plural = 'User Groups'

    def __str__(self):
        return f"{self.user.email} - {self.group.name}"
