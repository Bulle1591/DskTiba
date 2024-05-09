$(document).ready(function() {

    // Listen for the custom event when clicking an item from the item table
    $(document).on('itemClicked', function(event, itemId, itemName, itemQuantity) {
    // Check if the item has already been added in the initial rows or the newly added rows
    var isItemAlreadyAdded = false;
    $('#requisitionTable .item-name').each(function() {
        if ($(this).text() == itemName) {
            isItemAlreadyAdded = true;
            return false; // Exit the loop early since we found a match
        }
    });

    if (isItemAlreadyAdded) {
        // If the item exists in the formset, display a message to the user or handle it accordingly
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'This item already exists in the requisition. Please update or remove it before adding again.',
        });
    } else {
        // Check if the item is out of stock
        if (itemQuantity == 0) {
            Swal.fire({
                title: 'Out of Stock',
                text: itemName + " is out of stock. Would you like to create a Purchase Requisition?",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Create Purchase Requisition',
                cancelButtonText: 'Cancel'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Code to create a Purchase Requisition goes here
                }
            });
        } else {
            // If the item does not exist in the formset, proceed to add it
            // Get the current form count
            var formCount = $('#requisitionTable tr').length;

            // Create a new row
            var newRow = createNewRow(formCount);

            // Set the item details in the new requisition row
            newRow.find('.item-name').text(itemName);
            newRow.find('.item-quantity').text(itemQuantity);
            newRow.find('.item-id').val(itemId);

            // Append the new row to the requisition table
            $('#requisitionTable').append(newRow);

            // Update form indices and increment the TOTAL_FORMS count
            updateFormIndices();
        }
    }

    $.get('/get_department_item_quantity/', {item_id: itemId, user_id: currentUserId}, function(data) {
            var departmentQuantity = data.quantity;
            newRow.find('.department-quantity').text(departmentQuantity);
        });
    });


    function createNewRow(formCount) {
    // Create a new row
    var newRow = $('<tr class="item-formset new-row"></tr>');

    // Add the desired fields to the new row
    newRow.append('<td class="custom-td fv-row"><span class="item-name"></span><input type="hidden" class="item-id" name="items-' + formCount + '-item" id="id_items-' + formCount + '-item"><i class="float-end fas fa-edit tip edit" title="Edit" style="cursor:pointer;"></i></td>');
    newRow.append('<td class="fv-row"><span class="item-quantity"></span></td>');
    newRow.append('<td class="fv-row"><span class="department-quantity"></span></td>');
    newRow.append('<td class="fv-row"><input type="text" class="form-control" name="items-' + formCount + '-quantity" id="id_items-' + formCount + '-quantity"></td>');
    newRow.append('<td class="fv-row"><input type="text" class="form-control" rows="1" name="items-' + formCount + '-remark" id="id_items-' + formCount + '-remark"></td>');
    newRow.append('<td style="width: 30px !important; text-align: center;"><a class="remove-new-item" data-bs-toggle="tooltip" data-bs-placement="top" href="#" aria-label="Add" data-bs-original-title="Delete"><svg class="text-danger delete-icon" width="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path opacity="0.4" d="M19.643 9.48851C19.643 9.5565 19.11 16.2973 18.8056 19.1342C18.615 20.8751 17.4927 21.9311 15.8092 21.9611C14.5157 21.9901 13.2494 22.0001 12.0036 22.0001C10.6809 22.0001 9.38741 21.9901 8.13185 21.9611C6.50477 21.9221 5.38147 20.8451 5.20057 19.1342C4.88741 16.2873 4.36418 9.5565 4.35445 9.48851C4.34473 9.28351 4.41086 9.08852 4.54507 8.93053C4.67734 8.78453 4.86796 8.69653 5.06831 8.69653H18.9388C19.1382 8.69653 19.3191 8.78453 19.4621 8.93053C19.5953 9.08852 19.6624 9.28351 19.643 9.48851Z" fill="currentColor"></path><path d="M21 5.97686C21 5.56588 20.6761 5.24389 20.2871 5.24389H17.3714C16.7781 5.24389 16.2627 4.8219 16.1304 4.22692L15.967 3.49795C15.7385 2.61698 14.9498 2 14.0647 2H9.93624C9.0415 2 8.26054 2.61698 8.02323 3.54595L7.87054 4.22792C7.7373 4.8219 7.22185 5.24389 6.62957 5.24389H3.71385C3.32386 5.24389 3 5.56588 3 5.97686V6.35685C3 6.75783 3.32386 7.08982 3.71385 7.08982H20.2871C20.6761 7.08982 21 6.75783 21 6.35685V5.97686Z" fill="currentColor"></path></svg></a></td>');

    return newRow;
    }



    // When the delete icon is clicked in the requisition table
    $('#requisitionTable').on('click', '.delete-icon', function(e) {
        e.preventDefault();

        // Find the corresponding checkbox for deletion
        var checkboxId = $(this).closest('td').find('.delete-checkbox').attr('id');

        // Toggle the checkbox state
        $('#' + checkboxId).prop('checked', function(index, currentValue) {
            return !currentValue;
        });
    });


    // Remove initial row
    $('#requisitionTable').on('click', '.remove-initial-item', function(e) {
        e.preventDefault();

        var row = $(this).closest('tr');

        Swal.fire({
            title: 'Are you sure you want to delete this item?',
            text: "This action cannot be undone!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            if (result.isConfirmed) {
                row.find('input[name$="-DELETE"]').prop('checked', true);
                row.hide();
            }
        });
    });

    // Remove new empty row
    $('#requisitionTable').on('click', '.remove-new-item', function(e) {
        e.preventDefault();

        var row = $(this).closest('tr');
        row.remove();
        updateFormIndices(); // Update form indices and decrement the TOTAL_FORMS count
    });


    function updateFormIndices() {
        // Update the indices in the id and name attributes of all form elements
        var formCount = 0;
        $('#requisitionTable tr').each(function(index) {
            if ($(this).hasClass('item-formset')) {
                $(this).find(':input[id]').each(function() {  // Only select input elements that have an id
                    var id = $(this).attr('id').replace(/-\d+-/, '-' + formCount + '-');
                    var name = $(this).attr('name').replace(/-\d+-/, '-' + formCount + '-');
                    $(this).attr('id', id);
                    $(this).attr('name', name);
                });
                formCount++;
            }
        });

        // Count the current number of forms
        var formCount = $('#requisitionTable tr.item-formset').length;

        // Update the TOTAL_FORMS count
        $('#id_items-TOTAL_FORMS').val(formCount);
    }


    // Function to remove all rows and reset form fields without confirmation
    window.resetFormset = function() {
    // Remove only new empty rows
    $('#requisitionTable .item-formset:not(.initial-row)').remove();
    updateFormIndices();
    // Uncheck all checkboxes
    $('.item-checkbox').prop('checked', false);

    // Reset other fields
    $('#requisitionOrderForm').get(0).reset();

    // Reset Select2 fields
    $('#id_location').val(null).trigger('change');
    };

    // When the reset button is clicked in the requisition table, call the resetFormset function
    $('#resetFormsetButton').click(function(e) {
        e.preventDefault();
        window.resetFormset();
    });

});
