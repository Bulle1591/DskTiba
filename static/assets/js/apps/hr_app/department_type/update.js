$(document).ready(function() {
    // Assuming 'userGroupTable' is your DataTable
    $(document).on('click', '.edit-department-type', function (e) {
        e.preventDefault();

        // Get the row that contains the clicked button
        var row = departmentTypeTable.row($(this).parents('tr'));

        // Get the data for the row
        var data = row.data();

        // Load the data into the form
        $('#departmentTypeForm input[name="id"]').val(data.id); // Set the ID
        $('#departmentTypeForm input[name="name"]').val(data.name);
        $('#departmentTypeForm input[name="code"]').val(data.code);
        $('#departmentTypeForm select[name="status"]').val(data.status).trigger('change');

        // Change the title of the modal
        $('.form-title').text('Update Department Type');

        // Show the modal
        $('#departmentTypeModal').modal('show');
    });

    // Reset the title when the modal is hidden
    $('#departmentTypeModal').on('hidden.bs.modal', function (e) {
        $('.form-title').text('Create Department Type');
    });
});
