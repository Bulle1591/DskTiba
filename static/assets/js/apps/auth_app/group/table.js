// Declare the table as a global variable
var userGroupTable;

    $(document).ready(function () {
        /* Here begins the DataTable configuration. */
        if ($.fn.dataTable.isDataTable('#userGroupTable')) {
        $('#userGroupTable').DataTable().destroy();
    }

        userGroupTable = $('#userGroupTable').DataTable({
        // New initialization options...
        pageLength: 5,
        lengthMenu: [[5, 10, 25, 50, -1], [10, 25, 50, "All"]],
        retrieve: true,
        serverSide: false,
        processing: true,
        full_row_select: true,
        /* Set up the data source */
        ajax: {
            url: "/ajax_datatable/usergroup/"
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
            
            {name: "name", data: "name"},
//            {
//            name: "parent",
//            data: null,  // Use null for function-based data
//            render: function(data, type, row) {
//                // Check if parent exists, if not, display '-'
//                return data.parent ? data.parent : '-';
//                }
//            },
            {name: "description", data: "description"},
            {name: "status", data: "status_display"},

            {
                data: null,
                className: "text-center",
                defaultContent: `
                    <div>
                        <a class="btn btn-sm btn-icon text-primary flex-end edit-user-group" data-bs-toggle="tooltip" href="#" aria-label="Edit Role" data-bs-original-title="Edit Role">
                            <span class="btn-inner">
                                <svg width="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M11.4925 2.78906H7.75349C4.67849 2.78906 2.75049 4.96606 2.75049 8.04806V16.3621C2.75049 19.4441 4.66949 21.6211 7.75349 21.6211H16.5775C19.6625 21.6211 21.5815 19.4441 21.5815 16.3621V12.3341" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                    <path fill-rule="evenodd" clip-rule="evenodd" d="M8.82812 10.921L16.3011 3.44799C17.2321 2.51799 18.7411 2.51799 19.6721 3.44799L20.8891 4.66499C21.8201 5.59599 21.8201 7.10599 20.8891 8.03599L13.3801 15.545C12.9731 15.952 12.4211 16.181 11.8451 16.181H8.09912L8.19312 12.401C8.20712 11.845 8.43412 11.315 8.82812 10.921Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                    <path d="M15.1655 4.60254L19.7315 9.16854" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                </svg>
                            </span>
                        </a>
                        <a class="btn btn-sm btn-icon text-danger" data-bs-toggle="tooltip" href="#" aria-label="Delete Role" data-bs-original-title="Delete Role">
                            <span class="btn-inner">
                                <svg width="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="currentColor">
                                    <path d="M19.3248 9.46826C19.3248 9.46826 18.7818 16.2033 18.4668 19.0403C18.3168 20.3953 17.4798 21.1893 16.1088 21.2143C13.4998 21.2613 10.8878 21.2643 8.27979 21.2093C6.96079 21.1823 6.13779 20.3783 5.99079 19.0473C5.67379 16.1853 5.13379 9.46826 5.13379 9.46826" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                    <path d="M20.708 6.23975H3.75" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                    <path d="M17.4406 6.23973C16.6556 6.23973 15.9796 5.68473 15.8256 4.91573L15.5826 3.69973C15.4326 3.13873 14.9246 2.75073 14.3456 2.75073H10.1126C9.53358 2.75073 9.02558 3.13873 8.87558 3.69973L8.63258 4.91573C8.47858 5.68473 7.80258 6.23973 7.01758 6.23973" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                </svg>
                            </span>
                        </a>
                    </div>
                    `
            },
        ],

        rowCallback: function(row, data) {
        // Assign the ID of the data item to the row
        $(row).data('id', data.id);
        },
    });

    /* Add a checkbox in the header for selecting/deselecting all rows */
    $('#userGroupTable thead th:eq(0)').html('<input type="checkbox" id="select-all">');

    // Initially hide the delete button
    $('#delete-user-group').hide();


    /* Handle the select/deselect all functionality */
    $('#select-all').on('click', function() {
        var rows = userGroupTable.rows({ 'search': 'applied' }).nodes();
        $('input[type="checkbox"]', rows).prop('checked', this.checked);

        // Show or hide buttons based on whether any checkboxes are selected
        toggleButtons();
    });

     /* Update the select-all checkbox and show or hide buttons when a single checkbox is changed */
    $('#userGroupTable tbody').on('change', 'input[type="checkbox"]', function() {
        if (!this.checked) {
            var el = $('#select-all').get(0);
            if (el && el.checked && ('indeterminate' in el)) {
                el.indeterminate = true;
            }
        }

        // Show or hide buttons based on whether any checkboxes are selected
        toggleButtons();
    });

    $('#delete-user-group').on('click', function() {
    console.log('Delete button clicked');  // Add this line

    // Get the IDs of the selected user groups
    var selectedIds = $('#userGroupTable input[type="checkbox"]:checked').map(function() {
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
                    url: '/api/usergroup/delete/',  // URL for your delete view
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken  // Include the CSRF token in the request headers
                    },
                    data: { 'ids': selectedIds },
                    success: function(response) {
                        // Refresh the table and call toggleButtons after the table has reloaded
                        userGroupTable.ajax.reload(function() {
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
                $('#userGroupTable input[type="checkbox"]').prop('checked', false);
                // Show or hide buttons based on whether any checkboxes are selected
                toggleButtons();
            }
        });
    }
});


});


/* Show or hide buttons based on whether any checkboxes are selected */
function toggleButtons() {
    if ($('#userGroupTable input[type="checkbox"]:checked').length > 0) {
        // If any checkboxes are selected, show the delete button and hide the other buttons
        $('#delete-user-group').show();
        $('#add-user-group').hide();
        $('#add-user-permission').hide();
        $('#add-user-role').hide();
    } else {
        // If no checkboxes are selected, hide the delete button and show the other buttons
        $('#delete-user-group').hide();
        $('#add-user-group').show();
        $('#add-user-permission').show();
        $('#add-user-role').show();
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
