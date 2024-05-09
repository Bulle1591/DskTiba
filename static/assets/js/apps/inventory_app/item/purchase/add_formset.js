$(document).ready(function() {
    // Initialize the formset
    var formsetSelector = '.item-formset';
    var formsetPrefix = 'form'; // Update this to match your formset prefix

    // Get the options from the first 'item' select field
    var itemOptions = $('.item-select:first option').clone();

    // Get the options from the first 'location' select field
    var locationOptions = $('.location-select:first option').clone();

    // Function to update form indices and button visibility
    function updateFormIndices() {
        $(formsetSelector).each(function(index) {
            $(this).find('input, select, textarea').each(function() {
                var regex = new RegExp('(' + formsetPrefix + '-\\d+-)', 'g');
                var replacement = formsetPrefix + '-' + index + '-';
                if ($(this).attr('id')) {
                    $(this).attr({
                        'id': $(this).attr('id').replace(regex, replacement),
                        'name': $(this).attr('name').replace(regex, replacement)
                    });
                }
            });
        });

        // Show or hide the "Remove All" button
        if ($(formsetSelector).length > 2) {
            $('.remove-all-items').show();
        } else {
            $('.remove-all-items').hide();
        }
    }

    // Hide the "Remove All" button initially
    $('.remove-all-items').hide();


    // Function to create a new row
    function createNewRow(formCount) {
        // Create a new row
        var newRow = $('<tr class="item-formset"></tr>');

        // Add the desired fields to the new row
        newRow.append('<td class="custom-td"><select class="select2-basic-single form-select item-select" data-placeholder="Select an item" style="width: 100%;" name="form-' + formCount + '-item" id="id_form-' + formCount + '-item"></select><span class="item-name"></span><i class="float-end fas fa-edit tip edit" title="Edit" style="cursor:pointer;"></i></td>');
        newRow.append('<td><input type="text" class="form-control unit-price" name="form-' + formCount + '-unit_price" id="id_form-' + formCount + '-unit_price"></td>');
        newRow.append('<td><input type="text" class="form-control quantity" name="form-' + formCount + '-quantity" id="id_form-' + formCount + '-quantity"></td>');
        newRow.append('<td><input type="text" class="form-control flatpickrdate flatpickr-input active expire-date" placeholder="Select Date" data-id="minDate" readonly="readonly" id="id_form-' + formCount + '-expiration_date" name="form-' + formCount + '-expiration_date"></td>');
        newRow.append('<td><select class="select2-basic-single form-select location-select" data-placeholder="Select warehouse" style="width: 100%;" name="form-' + formCount + '-location" id="id_form-' + formCount + '-location"></select></td>');
        newRow.append('<td style="width: 30px !important; text-align: center;"><a class="remove-new-item" data-bs-toggle="tooltip" data-bs-placement="top" href="#" aria-label="Add" data-bs-original-title="Delete"><svg class="text-danger" width="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path opacity="0.4" d="M19.643 9.48851C19.643 9.5565 19.11 16.2973 18.8056 19.1342C18.615 20.8751 17.4927 21.9311 15.8092 21.9611C14.5157 21.9901 13.2494 22.0001 12.0036 22.0001C10.6809 22.0001 9.38741 21.9901 8.13185 21.9611C6.50477 21.9221 5.38147 20.8451 5.20057 19.1342C4.88741 16.2873 4.36418 9.5565 4.35445 9.48851C4.34473 9.28351 4.41086 9.08852 4.54507 8.93053C4.67734 8.78453 4.86796 8.69653 5.06831 8.69653H18.9388C19.1382 8.69653 19.3191 8.78453 19.4621 8.93053C19.5953 9.08852 19.6624 9.28351 19.643 9.48851Z" fill="currentColor"></path><path d="M21 5.97686C21 5.56588 20.6761 5.24389 20.2871 5.24389H17.3714C16.7781 5.24389 16.2627 4.8219 16.1304 4.22692L15.967 3.49795C15.7385 2.61698 14.9498 2 14.0647 2H9.93624C9.0415 2 8.26054 2.61698 8.02323 3.54595L7.87054 4.22792C7.7373 4.8219 7.22185 5.24389 6.62957 5.24389H3.71385C3.32386 5.24389 3 5.56588 3 5.97686V6.35685C3 6.75783 3.32386 7.08982 3.71385 7.08982H20.2871C20.6761 7.08982 21 6.75783 21 6.35685V5.97686Z" fill="currentColor"></path></svg></a></td>');

        // Add the item options to the new 'item' select field
        newRow.find('.item-select').append(itemOptions.clone());

        // Add the location options to the new 'location' select field
        newRow.find('.location-select').append(locationOptions.clone());

        // Initialize Select2 for the new row
        newRow.find('.item-select').select2();
        // Initialize Select2 for the new location field
        newRow.find('.location-select').select2();

        // Initialize Select2 for the new row
        var itemSelect = newRow.find('.item-select').select2();
        var locationSelect = newRow.find('.location-select').select2();

        // Reset the select fields
        itemSelect.val(null).trigger('change');
        locationSelect.val(null).trigger('change');

        // Initialize flatpickr for the new row
        newRow.find(".expire-date").flatpickr({
            // options here
        });

        return newRow;
    }


    // When the "Add New" button is clicked...
    $('.btn.add-new-item').click(function() {
        // Count the current number of forms
        var formCount = $('.item-formset').length;

        // Check if the maximum number of forms has been reached
        if (formCount >= 10) {
            // Show a Swal.fire message
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'You reached the maximum item forms.You cannot add more than 10 items!',
            });
        } else {
            // Create a new row
            var newRow = createNewRow(formCount); // Pass formCount here

            // Append the new row to the formset
            $('tbody.ui-sortable').append(newRow);

            // Update form indices
            updateFormIndices();

            // Increment the TOTAL_FORMS count
            $('#id_form-TOTAL_FORMS').val(formCount + 1);

            console.log('New form added. Total forms: ' + (formCount + 1));
        }
    });

    // When an item is selected...
    $(document).on('change', '.item-select', function(e) {
        // Get the selected item
        var selectedItem = $(this).val();

        // Get all selected items
        var selectedItems = $('.item-select').map(function() {
            return $(this).val();
        }).get();

        // Check if the selected item is already in the list
        var itemCount = selectedItems.filter(function(item) {
            return item === selectedItem;
        }).length;

        // If the item is in the list more than once, show a Swal.fire message
        if (itemCount > 1) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'This item has already been selected. Please choose a different item.',
            });

            // Remove the selected item
            $(this).val(null).trigger('change');
        }
    });



    // When the "Remove" button is clicked...
    $(document).on('click', '.remove-new-item', function() {
        // Check if this is the default row
        if ($(this).parents(formsetSelector).index() === 0) {
            // Show a Swal.fire message
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Default item form cannot be removed!',
            });
        } else {
            // Remove the parent form
            $(this).parents(formsetSelector).remove();

            // Update form indices
            updateFormIndices();

            // Decrement the TOTAL_FORMS count
            var formCount = $(formsetSelector).length;
            $('#id_form-TOTAL_FORMS').val(formCount);

            console.log('Form removed. Total forms: ' + formCount);
        }
    });

    // When the "Remove All" button is clicked...
    $('.btn.remove-all-items').click(function() {
        // Show a Swal.fire confirmation dialog
        Swal.fire({
            title: 'Are you sure?',
            text: "This action will remove all item forms except first default form!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, remove it!'
        }).then((result) => {
            if (result.isConfirmed) {
                // Remove all forms except the default one
                $(formsetSelector).not(':first').remove();

                // Update form indices
                updateFormIndices();

                // Update the TOTAL_FORMS count
                var formCount = $(formsetSelector).length;
                $('#id_form-TOTAL_FORMS').val(formCount);

                console.log('All forms removed. Total forms: ' + formCount);
            }
        });
    });
});