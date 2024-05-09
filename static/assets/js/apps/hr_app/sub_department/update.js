$(document).ready(function() {
    // Assuming 'userGroupTable' is your DataTable
    $(document).on('click', '.edit-sub-department', function (e) {
        e.preventDefault();

        // Get the row that contains the clicked button
        var row = subDepartmentTable.row($(this).parents('tr'));

        // Get the data for the row
        var data = row.data();

        // Load the data into the form
        $('#subDepartmentForm input[name="id"]').val(data.id); // Set the ID
        $('#subDepartmentForm input[name="title"]').val(data.title);
        $('#subDepartmentForm input[name="description"]').val(data.description);
        $('#subDepartmentForm select[name="status"]').val(data.status).trigger('change');

        // Change the title of the modal
        $('.form-title').text('Update Employment Type');

        // Show the modal
        $('#subDepartmentModal').modal('show');
    });

    // Reset the title when the modal is hidden
    $('#subDepartmentModal').on('hidden.bs.modal', function (e) {
        $('.form-title').text('Create Employment Type');
    });
});
