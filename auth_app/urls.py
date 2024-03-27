from django.urls import path
from .views import UserGroupDataView, UserGroupCRUDView, UserGroupDeleteView, PermissionCRUDView, PermissionDataView, \
    RoleCRUDView, RoleDataView, RoleCardView, RoleDetailView
# from . import ajax_datatable_views
from django.contrib.auth import views as auth_views

app_name = 'auth_app'

urlpatterns = [

    # AUTHENTICATION URLS
    path('', auth_views.LoginView.as_view(template_name='auth_app/login/signin.html'),
         name='login'),
    # USER GROUPS URLS
    path('api/usergroup/', UserGroupCRUDView.as_view(), name='usergroup'),
    path('ajax_datatable/usergroup/', UserGroupDataView.as_view(), name='usergroup_data'),
    # path('ajax_datatable/usergroup/', ajax_datatable_views.UserGroupAjaxDatatableView.as_view(),
    #      name="ajax_datatable_usergroups"),
    path('api/usergroup/delete/', UserGroupDeleteView.as_view(), name='usergroup_delete'),

    # PERMISSIONS URLS
    path('api/permission/', PermissionCRUDView.as_view(), name='permission'),
    path('ajax_datatable/permission/', PermissionDataView.as_view(), name='permission_data'),

    # ROLES URLS
    path('api/role/', RoleCRUDView.as_view(), name='role'),
    path('ajax_datatable/role/', RoleDataView.as_view(), name='role_data'),
    path('ajax_card/role/', RoleCardView.as_view(), name='ajax_card-role_data'),
    path('role/view/<int:id>/', RoleDetailView.as_view(), name='role_detail'),
]
