from django.contrib import admin
from .models import AppUser, Role, AppGroup, Permission, GroupPermission, AppUserGroup, FailedLoginAttempt


class AppUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff', 'role', 'date_joined', 'last_login']
    search_fields = ['email', 'first_name', 'last_name']
    readonly_fields = ['date_joined', 'last_login']


class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'user_count']
    search_fields = ['name']

    def user_count(self, obj):
        return obj.appuser_set.count()

    user_count.short_description = 'User Count'


class UserGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'status']
    search_fields = ['name']


class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'content_type', 'object_id']
    search_fields = ['name']


class GroupPermissionAdmin(admin.ModelAdmin):
    list_display = ['group', 'get_permissions']
    search_fields = ['group__name']

    def get_permissions(self, obj):
        return ", ".join([p.name for p in obj.permissions.all()])

    get_permissions.short_description = 'Permissions'


class AppUserGroupAdmin(admin.ModelAdmin):
    list_display = ['user', 'group']
    search_fields = ['user__email', 'group__name']


class FailedLoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('username', 'timestamp', 'attempt_type', 'ip_address')
    search_fields = ['username', 'ip_address']
    list_filter = ['attempt_type']


admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(AppGroup, UserGroupAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(GroupPermission, GroupPermissionAdmin)
admin.site.register(AppUserGroup, AppUserGroupAdmin)
admin.site.register(FailedLoginAttempt, FailedLoginAttemptAdmin)
