from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    DepartmentTypeCRUDView, DepartmentTypeDataView,
    DepartmentTypeDeleteView, DesignationCRUDView,
    DesignationDeleteView, DesignationDataView,
    JobTypeCRUDView, JobTypeDataView, JobTypeDeleteView,
    DepartmentCRUDView, DepartmentDataView, DepartmentDeleteView,
    SubDepartmentCRUDView, SubDepartmentDataView, EmployeeCreateView,
    EmployeeCardView, GenerateEmpNumberView

)

app_name = 'hr_app'

urlpatterns = [
                  # Department Type
                  path('department_type/', DepartmentTypeCRUDView.as_view(), name='department_type'),
                  path('ajax_datatable/department_type/', DepartmentTypeDataView.as_view(),
                       name='department_type_data'),
                  path('api/department_type/delete/', DepartmentTypeDeleteView.as_view(),
                       name='department_type_delete'),

                  # Designation
                  path('designation/', DesignationCRUDView.as_view(), name='designation'),
                  path('ajax_datatable/designation/', DesignationDataView.as_view(),
                       name='designation_data'),
                  path('api/designation/delete/', DesignationDeleteView.as_view(),
                       name='designation_delete'),

                  # Job Type
                  path('department/', DepartmentCRUDView.as_view(), name='department'),
                  path('ajax_datatable/department/', DepartmentDataView.as_view(),
                       name='department_data'),
                  path('api/department/delete/', DepartmentDeleteView.as_view(),
                       name='department_delete'),

                  # Department
                  path('job_type/', JobTypeCRUDView.as_view(), name='job_type'),
                  path('ajax_datatable/job_type/', JobTypeDataView.as_view(),
                       name='job_type_data'),
                  path('api/job_type/delete/', JobTypeDeleteView.as_view(),
                       name='job_type_delete'),

                  # Department
                  path('sub_department/', SubDepartmentCRUDView.as_view(), name='sub_department'),
                  path('ajax_datatable/sub_department/', SubDepartmentDataView.as_view(),
                       name='sub_department_data'),

                  # Employee
                  path('generate_emp_number/', GenerateEmpNumberView.as_view(), name='generate_emp_number'),
                  path('employee/', EmployeeCreateView.as_view(), name='employee'),
                  path('ajax_card/employee/', EmployeeCardView.as_view(), name='ajax_card-employee_data'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
