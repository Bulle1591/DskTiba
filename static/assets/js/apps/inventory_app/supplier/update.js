$(document).ready(function() {
    // Assuming 'userGroupTable' is your DataTable
    $(document).on('click', '.edit-supplier', function (e) {
        e.preventDefault();

        // Get the row that contains the clicked button
        var row = supplierTable.row($(this).parents('tr'));

        // Get the data for the row
        var data = row.data();

        // Load the data into the form
        $('#supplierForm input[name="id"]').val(data.id); // Set the ID
        $('#supplierForm input[name="name"]').val(data.name);
        $('#supplierForm input[name="contact_person"]').val(data.contact_person);
        $('#supplierForm input[name="contact_number"]').val(data.contact_number);
        $('#supplierForm input[name="email"]').val(data.email);
        $('#supplierForm textarea[name="address"]').val(data.address);


        // Change the title of the modal
        $('.form-title').text('Update Supplier');

        // Show the modal
        $('#supplierModal').modal('show');
    });

    // Reset the title when the modal is hidden
    $('#supplierModal').on('hidden.bs.modal', function (e) {
        $('.form-title').text('Create Supplier');
    });
});
