$(document).ready(function() {
    var debounceTimeout;

    function loadItems() {
    var searchQuery = $('#search_add_item').val();
    var categoryId = $('#item-category').val();

        $.ajax({
            url: '/ajax_datatable/item/',
            type: 'GET',
            data: {
                'search_query': searchQuery,
                'category_id': categoryId
            },
            dataType: 'json',
            success: function(data) {
                $('#itemDataTable tbody').empty();

                if (data.data.length === 0) {
                    var message = '';
                    if (!searchQuery && !categoryId) {
                        message = 'No items exist in the database. You cannot create a requisition.';
                        Swal.fire({
                            icon: 'warning',
                            title: 'No items',
                            text: message,
                            showConfirmButton: true
                        });
                    } else if (searchQuery && !categoryId) {
                        message = 'No items match your search query. Please try again!';
                    } else if (!searchQuery && categoryId) {
                        message = 'There are no items for the selected category. Contact Store Manager!';
                    } else {
                        message = 'No items match your search query in the selected category. Please try again!';
                    }

                    if (message !== 'No items exist in the database. You cannot create a requisition.') {
                        Swal.fire({
                            icon: 'warning',
                            title: 'No items',
                            text: message,
                            showConfirmButton: true
                        }).then(function() {
                            $('#search_add_item').val('');
                            $('#item-category').val('').trigger('change');
                            loadItems();
                        });
                    }
                } else {
                    data.data.forEach(function(item) {
                        var fullName = item.name;

                        if (item.strength) {
                            fullName += ' ' + item.strength;
                        } else if (item.unit_of_measure) {
                            fullName += ' ' + item.unit_of_measure;
                        }

                        $('#itemDataTable tbody').append(
                            '<tr>' +
                            '<td><input type="checkbox" class="item-checkbox" data-item-id="' + item.id + '"></td>' +
                            '<td>' + fullName + '</td>' +
                            '<td class="text-center">' + item.quantity_on_hand + '</td>' +
                            '</tr>'
                        );
                    });

                    // Unbind any existing click events
                    $('#itemDataTable tbody tr').off('click');

                    // Add click event to the new rows
                    $('#itemDataTable tbody tr').on('click', function() {
                        // Trigger a custom event and pass the item details
                        $(document).trigger('itemClicked', [$(this).find('.item-checkbox').data('item-id'), $(this).find('td:nth-child(2)').text(), $(this).find('td:nth-child(3)').text()]);
                    });
                }
            }
        });
    }


    loadItems();

    $('#search_add_item, #item-category').on('change', loadItems);

    $('#search_add_item').on('keyup', function() {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(loadItems, 500); // Adjust the delay as needed
    });
});
