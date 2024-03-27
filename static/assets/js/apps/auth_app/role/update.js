$(document).ready(function() {
    $(document).on('click', '.edit-role', function (e) {
        e.preventDefault();

        // Get the card that contains the clicked button
        var card = $(this).closest('.role-permission-card');

        // Get the role data from the card
        var roleId = $(this).data('role-id'); // Get the role ID from the button's data-role-id attribute
        var roleName = card.find('.role-name').text();
        var roleDescription = card.find('.role-description').text();

        var rolePermissionsData = $(this).data('role-permissions');
        var rolePermissions = typeof rolePermissionsData === 'string' ? JSON.parse(rolePermissionsData) : rolePermissionsData;

        console.log(rolePermissions); // log the rolePermissions array to the console

        // Now rolePermissions is an array of objects, you can map over it like this:
        var permissionIds = rolePermissions.map(function(permission) {
            return permission.id;
        }).join(',');


        // Load the role data into the form
        $('#RoleForm input[name="id"]').val(roleId);
        $('#RoleForm input[name="name"]').val(roleName);
        $('#RoleForm textarea[name="description"]').val(roleDescription);
        // Add any other fields you need

        // Uncheck all permissions
        $('#RoleForm input[name="permissions"]').prop('checked', false);

        // Check the permissions that the role has
        $.each(rolePermissions, function(index, permission) {
            console.log('Checking checkbox for permission:', permission.id);
            $('#RoleForm input[id="' + permission.id + '"]').prop('checked', true);
        });

        // Change the title of the modal
        $('.form-title').text('Update Role');

        // Show the modal
        $('#addRoleModal').modal('show');
    });

    // Load the roles when the page loads
    loadRoles();
});
