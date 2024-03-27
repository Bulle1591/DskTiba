# from ajax_datatable.views import AjaxDatatableView
# from .models import AppGroup


# class UserGroupAjaxDatatableView(AjaxDatatableView):
#     model = AppGroup
#     title = 'User Groups'
#     initial_order = [['name', 'asc'], ]  # Assuming you want to order by 'name' in ascending order
#     length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
#     search_values_separator = ''


#     column_defs = [
#         AjaxDatatableView.render_row_tools_column_def(),
#         {'name': 'id', 'visible': False, 'searchable': False},  # 'id' column won't be included in global search
#         {'name': 'name', 'visible': True, 'searchable': True},   # 'name' column is searchable
#         {'name': 'parent', 'visible': True, 'searchable': True},  # 'parent' column is searchable
#         {'name': 'description', 'visible': True, 'searchable': True},  # 'description' column is searchable
#         {'name': 'status', 'visible': True, 'searchable': True},  # 'status' column is searchable
#     ]