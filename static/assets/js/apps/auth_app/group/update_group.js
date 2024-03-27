$(document).ready(function() {
    // Assuming 'userGroupTable' is your DataTable
    $(document).on('click', '.edit-user-group', function (e) {
        e.preventDefault();

        // Get the row that contains the clicked button
        var row = userGroupTable.row($(this).parents('tr'));

        // Get the data for the row
        var data = row.data();

        // Load the data into the form
        $('#userGroupForm input[name="id"]').val(data.id); // Set the ID
        $('#userGroupForm input[name="name"]').val(data.name);
        $('#userGroupForm select[name="parent"]').val(data.parent_id).trigger('change');
        $('#userGroupForm textarea[name="description"]').val(data.description);
        $('#userGroupForm select[name="status"]').val(data.status).trigger('change');

        // Change the title of the modal
        $('.form-title').text('Update User Group');

        // Show the modal
        $('#userGroupModal').modal('show');
    });

    // Reset the title when the modal is hidden
    $('#userGroupModal').on('hidden.bs.modal', function (e) {
        $('.form-title').text('Create User Group');
    });
});
