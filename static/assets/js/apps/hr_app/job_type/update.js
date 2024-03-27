$(document).ready(function() {
    // Assuming 'userGroupTable' is your DataTable
    $(document).on('click', '.edit-job-type', function (e) {
        e.preventDefault();

        // Get the row that contains the clicked button
        var row = jobTypeTable.row($(this).parents('tr'));

        // Get the data for the row
        var data = row.data();

        // Load the data into the form
        $('#jobTypeForm input[name="id"]').val(data.id); // Set the ID
        $('#jobTypeForm input[name="title"]').val(data.title);
        $('#jobTypeForm input[name="description"]').val(data.description);
        $('#jobTypeForm select[name="status"]').val(data.status).trigger('change');

        // Change the title of the modal
        $('.form-title').text('Update Employment Type');

        // Show the modal
        $('#jobTypeModal').modal('show');
    });

    // Reset the title when the modal is hidden
    $('#jobTypeModal').on('hidden.bs.modal', function (e) {
        $('.form-title').text('Create Employment Type');
    });
});
