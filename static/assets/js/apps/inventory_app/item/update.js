$(document).ready(function() {
    // Assuming 'itemTable' is your DataTable
    $(document).on('click', '.edit-item', function (e) {
        e.preventDefault();

        // Get the row that contains the clicked button
        var row = itemTable.row($(this).parents('tr'));

        // Get the data for the row
        var data = row.data();

        console.log(data.brand_name, data.name, data.category, data.subcategory);


        // Load the data into the form
        $('#itemForm input[name="id"]').val(data.id); // Set the ID
        $('#itemForm input[name="name"]').val(data.name);
        $('#itemForm textarea[name="description"]').val(data.description);
        $('#itemForm input[name="quantity_on_hand"]').val(data.quantity_on_hand);
        $('#itemForm input[name="reorder_level"]').val(data.reorder_level);
        $('#itemForm input[name="alert_quantity"]').val(data.alert_quantity);
        $('#itemForm input[name="unit_of_measure"]').val(data.unit_of_measure);
        $('#itemForm input[name="brand_name"]').val(data.brand_name);
        $('#itemForm input[name="strength"]').val(data.strength);
        $('#itemForm input[name="requires_prescription"]').prop('checked', data.requires_prescription);
        $('#itemForm input[name="can_be_sold"]').prop('checked', data.can_be_sold);
        $('#itemForm textarea[name="storage_conditions"]').val(data.storage_conditions);

        // Set the value for item_type, dosage_form, category, subcategory, and supplier
        $('#itemForm select[name="item_type"]').val(data.item_type).trigger('change');
        $('#itemForm select[name="dosage_form"]').val(data.dosage_form).trigger('change');
        $('#itemForm select[name="category"]').val(data.category_id).trigger('change');
        $('#itemForm select[name="subcategory"]').val(data.subcategory_id).trigger('change');
        $('#itemForm select[name="supplier"]').val(data.supplier_id).trigger('change');

        // Change the title of the modal
        $('.form-title').text('Update Item');

        // Show the modal
        $('#itemModal').modal('show');
    });

    // Reset the title when the modal is hidden
    $('#itemModal').on('hidden.bs.modal', function (e) {
        $('.form-title').text('Create Item');
    });
});
