// Declare the table as a global variable
var purchaseOrderTable;

    $(document).ready(function () {
        /* Here begins the DataTable configuration. */
        if ($.fn.dataTable.isDataTable('#purchaseOrderTable')) {
        $('#purchaseOrderTable').DataTable().destroy();
    }

        purchaseOrderTable = $('#purchaseOrderTable').DataTable({
        // New initialization options...
        pageLength: 7,
        lengthMenu: [[7, 10, 25, 50, -1], [7, 10, 25, 50, "All"]],
        retrieve: true,
        serverSide: false,
        processing: true,
        full_row_select: true,
        /* Set up the data source */
         ajax: {
            url: "/ajax_datatable/purchased/orders/",
            data: function(d) {
                d.item_type = $('#item-type-filter').val();
                d.category_id = $('#category-filter').val();
                d.subcategory_id = $('#subcategory-filter').val();
                d.dosage_form = $('#dosage-form-filter').val(); // Add this line
            }
        },
        /* And set up the columns. Note that they must be identified by a "name" attribute,
           with the value matching the columns in your Django view. The "data" attribute selects which record value will be used,
           and should be the same value than for the "name" attribute. */
        columns: [
            {
                data: null,
                defaultContent: '<input type="checkbox" class="select-row">',
                orderable: false
            },

            { "data": "order_id" },
            {
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": '<button type="button" class="btn btn-sm btn-soft-primary" style="width: 100%;" data-bs-content="" title="Summary">Summary</button>'
            },

            { "data": "supplier" },
            { "data": "total_cost" },
            { "data": "order_date" },
            {
            "data": "status",
            "render": function ( data, type, row, meta ) {
                if(type === 'display'){
                    if(data == 'Draft'){
                        return '<span class="badge bg-soft-warning">' + data + '</span>';
                    } else if(data == 'Fulfilled'){
                        return '<span class="badge bg-soft-success">' + data + '</span>';
                    } else if(data == 'Canceled'){
                        return '<span class="badge bg-soft-danger">' + data + '</span>';
                    }
                }
                return data;
            }
            },
           {
            data: null,
            className: "center",
            render: function(data, type, row) {
                var buttons = '';

                if (row.status.toLowerCase() == 'draft') {
                    // If it's a draft, show Edit and Delete buttons
                    buttons = `
                        <div class="d-flex justify-content-center list-user-action">
                        <a class="btn btn-sm btn-icon btn-outline-warning me-1 edit-item" data-bs-toggle="tooltip" data-bs-placement="top" data-original-title="Edit" href="/purchase_order/edit/${row.id}/" aria-label="Edit" data-bs-original-title="Edit">
                          <span class="btn-inner">
                            <svg class="icon-20" width="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M11.4925 2.78906H7.75349C4.67849 2.78906 2.75049 4.96606 2.75049 8.04806V16.3621C2.75049 19.4441 4.66949 21.6211 7.75349 21.6211H16.5775C19.6625 21.6211 21.5815 19.4441 21.5815 16.3621V12.3341" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                <path fill-rule="evenodd" clip-rule="evenodd" d="M8.82812 10.921L16.3011 3.44799C17.2321 2.51799 18.7411 2.51799 19.6721 3.44799L20.8891 4.66499C21.8201 5.59599 21.8201 7.10599 20.8891 8.03599L13.3801 15.545C12.9731 15.952 12.4211 16.181 11.8451 16.181H8.09912L8.19312 12.401C8.20712 11.845 8.43412 11.315 8.82812 10.921Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                <path d="M15.1655 4.60254L19.7315 9.16854" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                             </svg>
                          </span>
                       </a>
                       <a class="btn btn-sm btn-icon btn btn-outline-danger" data-bs-toggle="tooltip" data-bs-placement="top" href="#" aria-label="Delete" data-bs-original-title="Delete">
                          <span class="btn-inner">
                            <svg class="icon-20" width="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="currentColor">
                                <path d="M19.3248 9.46826C19.3248 9.46826 18.7818 16.2033 18.4668 19.0403C18.3168 20.3953 17.4798 21.1893 16.1088 21.2143C13.4998 21.2613 10.8878 21.2643 8.27979 21.2093C6.96079 21.1823 6.13779 20.3783 5.99079 19.0473C5.67379 16.1853 5.13379 9.46826 5.13379 9.46826" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                <path d="M20.708 6.23975H3.75" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                <path d="M17.4406 6.23973C16.6556 6.23973 15.9796 5.68473 15.8256 4.91573L15.5826 3.69973C15.4326 3.13873 14.9246 2.75073 14.3456 2.75073H10.1126C9.53358 2.75073 9.02558 3.13873 8.87558 3.69973L8.63258 4.91573C8.47858 5.68473 7.80258 6.23973 7.01758 6.23973" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                             </svg>
                          </span>
                       </a>
                        </div>`;
                } else if (row.status.toLowerCase() == 'fulfilled') {
                    // If it's not a draft and status is pending, show Approve and Reject buttons
                    buttons = `
                        <div class="d-flex justify-content-center list-user-action">
                        <a class="btn btn-sm btn-icon btn-outline-success me-1" data-bs-toggle="tooltip" data-bs-placement="top" href="#" aria-label="Add" data-bs-original-title="Add">
                          <span class="btn-inner">

                          </span>
                       </a>
                       <a class="btn btn-sm btn-icon btn-outline-primary" data-bs-toggle="tooltip" data-bs-placement="top" href="#" aria-label="Add" data-bs-original-title="Add">
                          <span class="btn-inner">

                          </span>
                       </a>
                        </div>`;
                }

                return buttons;
            }
        }
        ],

        rowCallback: function(row, data) {
        // Assign the ID of the data item to the row
        $(row).data('id', data.id);
        },
    });

    // Add event listener for opening and closing details(USE POPUPS)
   $('#purchaseOrderTable tbody').on('click', 'td.details-control', function (e) {
    e.stopPropagation(); // Prevent the click event from propagating up to the document

    var tr = $(this).closest('tr');
    var row = purchaseOrderTable.row(tr);

    // Hide any other shown popovers
    $('.popover').not(this).popover('hide');

    // If the popover is not initialized, create the items list and initialize the popover.
    var items = '';
    for (var i = 0; i < row.data().items.length; i++) {
        items += (i+1) + '. <a href="/item-details/' + row.data().items[i].id + '" class="item-link" data-item-id="' + row.data().items[i].id + '">Name: ' + row.data().items[i].item_name + ', Quantity: ' + row.data().items[i].quantity + ', Unit Price: ' + row.data().items[i].unit_price + '</a><br>';
    }

    $(this).attr('data-bs-content', items);
    $(this).popover({
        trigger: 'focus', // Change this to 'manual'
        html: true,
        placement: 'top'
    }).popover('show');
    });

    // Hide popovers when clicking anywhere else in the document
    $(document).on('click', function (e) {
        $('[data-bs-toggle="popover"]').each(function () {
            // Only hide the popover if the click event target is not a child of the popover
            if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
                $(this).popover('hide');
            }
        });
    });

     // This script listens for changes in the item type, category, and subcategory filters.
    // When the selected value of any of these filters changes, it reloads the DataTable.
    // This means it makes a new AJAX request to the server with the updated filter values,
    // and then redraws the table with the new data.
    $('#item-type-filter, #category-filter, #subcategory-filter, #dosage-form-filter').change(function() {
        purchaseOrderTable.ajax.reload();
    });

    // Hide the dosage form filter initially
    // Initialize the select2 dropdowns
    $('#item-type-filter, #category-filter, #subcategory-filter, #dosage-form-filter').select2();

    // Hide the dosage form filter initially
    $('#dosage-form-filter').closest('.select2').hide();

    // This script listens for changes in the category filter.
    // When the selected category is 'Pharmaceuticals', it shows the dosage form filter dropdown.
    // Otherwise, it hides the dropdown.
    // This is useful if you want to show additional filters based on the selected category.
    $('#category-filter').change(function() {
    var selectedCategory = $("#category-filter option:selected").text();
    if (selectedCategory == 'Pharmaceuticals') {
        $('#dosage-form-filter').closest('.select2').show();
    } else {
        $('#dosage-form-filter').closest('.select2').hide();
    }
    });


    /* Add a checkbox in the header for selecting/deselecting all rows */
    $('#purchaseOrderTable thead th:eq(0)').html('<input type="checkbox" id="select-all">');

    // Initially hide the delete button
    $('#delete-item').hide();


    /* Handle the select/deselect all functionality */
    $('#select-all').on('click', function() {
        var rows = purchaseOrderTable.rows({ 'search': 'applied' }).nodes();
        $('input[type="checkbox"]', rows).prop('checked', this.checked);

        // Show or hide buttons based on whether any checkboxes are selected
        toggleButtons();
    });

     /* Update the select-all checkbox and show or hide buttons when a single checkbox is changed */
    $('#purchaseOrderTable tbody').on('change', 'input[type="checkbox"]', function() {
        if (!this.checked) {
            var el = $('#select-all').get(0);
            if (el && el.checked && ('indeterminate' in el)) {
                el.indeterminate = true;
            }
        }

        // Show or hide buttons based on whether any checkboxes are selected
        toggleButtons();
    });


    $('#delete-item').on('click', function() {
    console.log('Delete button clicked');  // Add this line

    // Get the IDs of the selected user groups
    var selectedIds = $('#purchaseOrderTable input[type="checkbox"]:checked').map(function() {
        return $(this).closest('tr').data('id');
    }).get();

    console.log('Selected IDs:', selectedIds);  // Add this line

    if (selectedIds.length > 0) {
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            buttonsStyling: false,
            confirmButtonText: 'Yes, delete it!',
            cancelButtonText: "No, return",
            customClass: {
                  confirmButton: "btn btn-sm btn-100 btn-danger",
                  cancelButton: "btn btn-sm btn-100 btn-active-light"
              }
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: '/item/delete/',  // URL for your delete view
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken  // Include the CSRF token in the request headers
                    },
                    data: { 'ids': selectedIds },
                    success: function(response) {
                        // Refresh the table and call toggleButtons after the table has reloaded
                        purchaseOrderTable.ajax.reload(function() {
                            // Show or hide buttons based on whether any checkboxes are selected
                            toggleButtons();
                        }, false);

                        // Show the success message
                        Swal.fire({
                            title: 'Success!',
                            text: response.message,
                            icon: 'success'
                        });
                    }
                });
            } else {
                // Uncheck all checkboxes when the cancel button is clicked
                $('#purchaseOrderTable input[type="checkbox"]').prop('checked', false);
                // Show or hide buttons based on whether any checkboxes are selected
                toggleButtons();
            }
        });
    }
});

/* Approve Purchase order form Pending to Fulfilled */
$('.approve-button').click(function() {
    var purchaseOrderId = $(this).data('id');
    $.post('/purchase_order/' + purchaseOrderId + '/approve/', function(response) {
        if (response.success) {
            // Update the status of the purchase order in the table
            $('#status-' + purchaseOrderId).text('Fulfilled');
        }
    });
});


});


/* Show or hide buttons based on whether any checkboxes are selected */
function toggleButtons() {
    if ($('#purchaseOrderTable input[type="checkbox"]:checked').length > 0) {
        // If any checkboxes are selected, show the delete button and hide the other buttons
        $('#delete-item').show();
    } else {
        // If no checkboxes are selected, hide the delete button and show the other buttons
        $('#delete-item').hide();
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
