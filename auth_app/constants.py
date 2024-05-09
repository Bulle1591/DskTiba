MODEL_NAMES = {
    'administration | logentry': 'Log [ Entry ]',
    'auth_app | appgroup': 'Groups',
    'auth_app | failedloginattempt': 'Failed Login',
    'auth_app | permission': 'Permissions',
    'auth_app | role': 'Roles',
    'auth_app | appuser': 'Users',
    'auth_app | grouppermission': 'Group Permissions',
    'auth_app | appusergroup': 'User Group',
    'hr_app | department': 'Department',
    'hr_app | departmenttype': 'Department Type',
    'hr_app | employeedocument': 'Employee Document',
    'hr_app | employeecontact': 'Employee Contacts',
    'hr_app | employeephoto': 'Employee Photo',
    'hr_app | jobtype': 'Employment Type',
    'hr_app | subdepartmentmaster': 'Sub-Department',
    'hr_app | employee': 'Employee',
    'hr_app | designation': 'Designation',
    # Add more mappings as needed

    'inventory_app | item': 'Item',
    'inventory_app | itemcategory': 'Item Category',
    'inventory_app | supplier': 'Supplier',
    'inventory_app | location': 'Warehouse/Location',
    'inventory_app | itemrequisition': 'Item Requisition',
    'inventory_app | itemrequisitionitem': 'Requested Items',
    'inventory_app | itemsubcategory': 'Item Sub-Category',
}


def get_model_name(app_label, model):
    key = f'{app_label} | {model}'
    return MODEL_NAMES.get(key, key)
