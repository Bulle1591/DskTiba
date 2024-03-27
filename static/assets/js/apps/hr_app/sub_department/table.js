// Declare the table as a global variable
var subDepartmentTable;

    $(document).ready(function () {
        /* Here begins the DataTable configuration. */
        if ($.fn.dataTable.isDataTable('#subDepartmentTable')) {
        $('#subDepartmentTable').DataTable().destroy();
    }

        subDepartmentTable = $('#subDepartmentTable').DataTable({
        // New initialization options...
        pageLength: 7,
        lengthMenu: [[7, 10, 25, 50, -1], [7, 10, 25, 50, "All"]],
        retrieve: true,
        serverSide: false,
        processing: true,
        full_row_select: true,
        /* Set up the data source */
        ajax: {
            url: "/ajax_datatable/sub_department/"
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
            {name: "department", data: "department"},
            {name: "department_types", data: "department_types"},
            {name: "status", data: "status_display"},
            {
                data: null,
                className: "center",
                defaultContent: `
                    <div class="d-flex justify-content-center">
                        <button class="btn btn-primary btn-icon btn-sm rounded-pill" role="button">
                            <span class="btn-inner">
                                <!-- SVG for the first button -->
                                <svg class="icon-32" width="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path opacity="0.4" d="M21.101 9.58786H19.8979V8.41162C19.8979 7.90945 19.4952 7.5 18.999 7.5C18.5038 7.5 18.1 7.90945 18.1 8.41162V9.58786H16.899C16.4027 9.58786 16 9.99731 16 10.4995C16 11.0016 16.4027 11.4111 16.899 11.4111H18.1V12.5884C18.1 13.0906 18.5038 13.5 18.999 13.5C19.4952 13.5 19.8979 13.0906 19.8979 12.5884V11.4111H21.101C21.5962 11.4111 22 11.0016 22 10.4995C22 9.99731 21.5962 9.58786 21.101 9.58786Z" fill="currentColor"></path>
                                    <path d="M9.5 15.0156C5.45422 15.0156 2 15.6625 2 18.2467C2 20.83 5.4332 21.5001 9.5 21.5001C13.5448 21.5001 17 20.8533 17 18.269C17 15.6848 13.5668 15.0156 9.5 15.0156Z" fill="currentColor"></path>
                                    <path opacity="0.4" d="M9.50023 12.5542C12.2548 12.5542 14.4629 10.3177 14.4629 7.52761C14.4629 4.73754 12.2548 2.5 9.50023 2.5C6.74566 2.5 4.5376 4.73754 4.5376 7.52761C4.5376 10.3177 6.74566 12.5542 9.50023 12.5542Z" fill="currentColor"></path>
                                </svg>
                            </span>
                        </button>
                        <button class="btn btn-primary btn-icon btn-sm rounded-pill ms-2 edit-sub-department" role="button">
                            <span class="btn-inner">
                                <!-- SVG for the second button -->
                                <svg class="icon-32" width="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path opacity="0.4" d="M19.9927 18.9534H14.2984C13.7429 18.9534 13.291 19.4124 13.291 19.9767C13.291 20.5422 13.7429 21.0001 14.2984 21.0001H19.9927C20.5483 21.0001 21.0001 20.5422 21.0001 19.9767C21.0001 19.4124 20.5483 18.9534 19.9927 18.9534Z" fill="currentColor"></path>
                                    <path d="M10.309 6.90385L15.7049 11.2639C15.835 11.3682 15.8573 11.5596 15.7557 11.6929L9.35874 20.0282C8.95662 20.5431 8.36402 20.8344 7.72908 20.8452L4.23696 20.8882C4.05071 20.8903 3.88775 20.7613 3.84542 20.5764L3.05175 17.1258C2.91419 16.4915 3.05175 15.8358 3.45388 15.3306L9.88256 6.95545C9.98627 6.82108 10.1778 6.79743 10.309 6.90385Z" fill="currentColor"></path>
                                    <path opacity="0.4" d="M18.1208 8.66544L17.0806 9.96401C16.9758 10.0962 16.7874 10.1177 16.6573 10.0124C15.3927 8.98901 12.1545 6.36285 11.2561 5.63509C11.1249 5.52759 11.1069 5.33625 11.2127 5.20295L12.2159 3.95706C13.126 2.78534 14.7133 2.67784 15.9938 3.69906L17.4647 4.87078C18.0679 5.34377 18.47 5.96726 18.6076 6.62299C18.7663 7.3443 18.597 8.0527 18.1208 8.66544Z" fill="currentColor"></path>
                                </svg>
                            </span>
                        </button>
                    </div>`
            },
        ],

        rowCallback: function(row, data) {
        // Assign the ID of the data item to the row
        $(row).data('id', data.id);
        },
    });

    /* Add a checkbox in the header for selecting/deselecting all rows */
    $('#subDepartmentTable thead th:eq(0)').html('<input type="checkbox" id="select-all">');

    // Initially hide the delete button
    $('#delete-sub-department').hide();


    /* Handle the select/deselect all functionality */
    $('#select-all').on('click', function() {
        var rows = subDepartmentTable.rows({ 'search': 'applied' }).nodes();
        $('input[type="checkbox"]', rows).prop('checked', this.checked);

        // Show or hide buttons based on whether any checkboxes are selected
        toggleButtons();
    });

     /* Update the select-all checkbox and show or hide buttons when a single checkbox is changed */
    $('#subDepartmentTable tbody').on('change', 'input[type="checkbox"]', function() {
        if (!this.checked) {
            var el = $('#select-all').get(0);
            if (el && el.checked && ('indeterminate' in el)) {
                el.indeterminate = true;
            }
        }

        // Show or hide buttons based on whether any checkboxes are selected
        toggleButtons();
    });

    $('#delete-job_type').on('click', function() {
    console.log('Delete button clicked');  // Add this line

    // Get the IDs of the selected user groups
    var selectedIds = $('#subDepartmentTable input[type="checkbox"]:checked').map(function() {
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
                    url: '/api/job_type/delete/',  // URL for your delete view
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken  // Include the CSRF token in the request headers
                    },
                    data: { 'ids': selectedIds },
                    success: function(response) {
                        // Refresh the table and call toggleButtons after the table has reloaded
                        subDepartmentTable.ajax.reload(function() {
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
                $('#subDepartmentTable input[type="checkbox"]').prop('checked', false);
                // Show or hide buttons based on whether any checkboxes are selected
                toggleButtons();
            }
        });
    }
});


});


/* Show or hide buttons based on whether any checkboxes are selected */
function toggleButtons() {
    if ($('#jobTypeTable input[type="checkbox"]:checked').length > 0) {
        // If any checkboxes are selected, show the delete button and hide the other buttons
        $('#delete-sub-department').show();
        $('#add-sub-department').hide();
        $('#department-page').hide();
    } else {
        // If no checkboxes are selected, hide the delete button and show the other buttons
        $('#delete-sub-department').hide();
        $('#add-sub-department').show();
        $('#department-page').show();
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
