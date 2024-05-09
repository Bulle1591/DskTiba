$(document).ready(function() {
    // Assuming 'locationTable' is your DataTable
    $(document).on('click', '.edit-location', function (e) {
        e.preventDefault();

        // Get the row that contains the clicked button
        var row = locationTable.row($(this).parents('tr'));

        // Get the data for the row
        var data = row.data();

        console.log(data.department, data.sub_department);

        // Load the data into the form

        $('#locationForm input[name="id"]').val(data.id); // Set the ID
        $('#locationForm input[name="name"]').val(data.name);

        // Set the value for department and sub_department
        $('#locationForm select[name="department"]').val(data.department_id).trigger('change');
        $('#locationForm select[name="sub_department"]').val(data.sub_department_id).trigger('change');





        // Change the title of the modal
        $('.form-title').text('Update Location');

        // Show the modal
        $('#locationModal').modal('show');
    });

    // Reset the title when the modal is hidden
    $('#locationModal').on('hidden.bs.modal', function (e) {
        $('.form-title').text('Create Location');
    });
});
