$(document).ready(function() {
    // Assuming 'itemCategoryTable' is your DataTable
    $(document).on('click', '.edit-item-category', function (e) {
        e.preventDefault();

        // Get the row that contains the clicked button
        var row = itemCategoryTable.row($(this).parents('tr'));

        // Get the data for the row
        var data = row.data();

        // Load the data into the form

        $('#itemCategoryForm input[name="id"]').val(data.id); // Set the ID
        $('#itemCategoryForm input[name="name"]').val(data.name);
        $('#itemCategoryForm textarea[name="description"]').val(data.description);


        // Change the title of the modal
        $('.form-title').text('Update Item Category');

        // Show the modal
        $('#itemCategoryModal').modal('show');
    });

    // Reset the title when the modal is hidden
    $('#itemCategoryModal').on('hidden.bs.modal', function (e) {
        $('.form-title').text('Create Item Category');
    });
});
