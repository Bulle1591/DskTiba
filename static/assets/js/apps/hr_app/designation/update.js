$(document).ready(function() {
    // Assuming 'userGroupTable' is your DataTable
    $(document).on('click', '.edit-designation', function (e) {
        e.preventDefault();

        // Get the row that contains the clicked button
        var row = designationTable.row($(this).parents('tr'));

        // Get the data for the row
        var data = row.data();

        // Load the data into the form
        $('#designationForm input[name="id"]').val(data.id); // Set the ID
        $('#designationForm input[name="title"]').val(data.title);
        $('#designationForm input[name="description"]').val(data.description);
        $('#designationForm select[name="status"]').val(data.status).trigger('change');

        // Change the title of the modal
        $('.form-title').text('Update Designation');

        // Show the modal
        $('#designationModal').modal('show');
    });

    // Reset the title when the modal is hidden
    $('#designationModal').on('hidden.bs.modal', function (e) {
        $('.form-title').text('Create Designation');
    });
});
