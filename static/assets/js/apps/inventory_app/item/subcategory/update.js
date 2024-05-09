$(document).ready(function() {
    // Assuming 'itemSubcategoryTable' is your DataTable
    $(document).on('click', '.edit-item-subcategory', function (e) {
        e.preventDefault();

        // Get the row that contains the clicked button
        var row = itemSubcategoryTable.row($(this).parents('tr'));

        // Get the data for the row
        var data = row.data();

        // Load the data into the form

        $('#itemSubcategoryForm input[name="id"]').val(data.id); // Set the ID
        $('#itemSubcategoryForm input[name="name"]').val(data.name);
        $('#itemSubcategoryForm select[name="category"]').val(data.category_id).trigger('change');
        $('#itemSubcategoryForm textarea[name="description"]').val(data.description);


        // Change the title of the modal
        $('.form-title').text('Update Item Subcategory');

        // Show the modal
        $('#itemSubcategoryModal').modal('show');
    });

    // Reset the title when the modal is hidden
    $('#itemSubcategoryModal').on('hidden.bs.modal', function (e) {
        $('.form-title').text('Create Item Subcategory');
    });
});
