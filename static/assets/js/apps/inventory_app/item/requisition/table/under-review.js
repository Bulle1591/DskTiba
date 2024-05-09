// Declare the table as a global variable
var underReviewRequisitionTable;

$(document).ready(function () {
    /* Here begins the DataTable configuration. */
    if ($.fn.dataTable.isDataTable('#underReviewRequisitionTable')) {
        $('#underReviewRequisitionTable').DataTable().destroy();
    }

    underReviewRequisitionTable = $('#underReviewRequisitionTable').DataTable({
        // New initialization options...
        pageLength: 7,
        lengthMenu: [[7, 10, 25, 50, -1], [7, 10, 25, 50, "All"]],
        retrieve: true,
        serverSide: false,
        processing: true,
        full_row_select: true,
        /* Set up the data source */
        ajax: {
            url: "/ajax_datatable/requisitions/under-review/", // Update the URL to point to the endpoint for draft requisitions
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
                {
                    name: "name",
                    data: "requisition_id",
                    render: function ( data, type, row, meta ) {
                        if(type === 'display'){
                            return '<a href="#" data-id="' + row.id + '" onclick="showUnderReviewRequisitionDetails(this)">' + data + '</a>';
                        }
                        return data;
                    }
                },
                { name: "requisition_type", data: "requisition_type" },
                {
                    "className": 'details-control',
                    "orderable": false,
                    "data": null,
                    "defaultContent": '<button type="button" class="btn btn-sm btn-soft-primary" style="width: 100%;" data-bs-content="" title="Summary">Summary</button>'
                },

                { name: "issuer", data: "issuer" },
                { name: "sub_department", data: "sub_department" },
                { name: "requested_by", data: "requested_by" },
                { name: "requested_at", data: "requested_at" },
                {
                    "data": "approval_status",
                    "render": function ( data, type, row, meta ) {
                        if(type === 'display' && data == 'Under Review'){
                            return '<span class="badge bg-success">' + data + '</span>';
                        }
                        return data;
                    }
                },
                {
                    data: null,
                    className: "center",
                    render: function(data, type, row) {
                        var buttons = `
                            <div class="d-flex justify-content-center list-user-action">
                            <a class="btn btn-sm btn-icon btn-info me-1" data-bs-toggle="tooltip" data-bs-placement="top" href="#" aria-label="Button 1" data-bs-original-title="Button 1">
                              <span class="btn-inner">
                                    <svg class="icon-20" width="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path opacity="0.4" fill-rule="evenodd" clip-rule="evenodd" d="M17.7366 6.04606C19.4439 7.36388 20.8976 9.29455 21.9415 11.7091C22.0195 11.8924 22.0195 12.1067 21.9415 12.2812C19.8537 17.1103 16.1366 20 12 20H11.9902C7.86341 20 4.14634 17.1103 2.05854 12.2812C1.98049 12.1067 1.98049 11.8924 2.05854 11.7091C4.14634 6.87903 7.86341 4 11.9902 4H12C14.0683 4 16.0293 4.71758 17.7366 6.04606ZM8.09756 12C8.09756 14.1333 9.8439 15.8691 12 15.8691C14.1463 15.8691 15.8927 14.1333 15.8927 12C15.8927 9.85697 14.1463 8.12121 12 8.12121C9.8439 8.12121 8.09756 9.85697 8.09756 12Z" fill="currentColor"></path>                                <path d="M14.4308 11.997C14.4308 13.3255 13.3381 14.4115 12.0015 14.4115C10.6552 14.4115 9.5625 13.3255 9.5625 11.997C9.5625 11.8321 9.58201 11.678 9.61128 11.5228H9.66006C10.743 11.5228 11.621 10.6695 11.6601 9.60184C11.7674 9.58342 11.8845 9.57275 12.0015 9.57275C13.3381 9.57275 14.4308 10.6588 14.4308 11.997Z" fill="currentColor">
                                    </path>
                                    </svg>
                              </span>
                           </a>
                           <a class="btn btn-sm btn-icon btn-primary" data-bs-toggle="tooltip" data-bs-placement="top" href="#" aria-label="Button 2" data-bs-original-title="Button 2">
                              <span class="btn-inner">
                                    <svg class="icon-32" width="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path opacity="0.4" d="M16.34 1.99976H7.67C4.28 1.99976 2 4.37976 2 7.91976V16.0898C2 19.6198 4.28 21.9998 7.67 21.9998H16.34C19.73 21.9998 22 19.6198 22 16.0898V7.91976C22 4.37976 19.73 1.99976 16.34 1.99976Z" fill="currentColor"></path>                                <path fill-rule="evenodd" clip-rule="evenodd" d="M11.1246 8.18921C11.1246 8.67121 11.5156 9.06421 11.9946 9.06421C12.4876 9.06421 12.8796 8.67121 12.8796 8.18921C12.8796 7.70721 12.4876 7.31421 12.0046 7.31421C11.5196 7.31421 11.1246 7.70721 11.1246 8.18921ZM12.8696 11.362C12.8696 10.88 12.4766 10.487 11.9946 10.487C11.5126 10.487 11.1196 10.88 11.1196 11.362V15.782C11.1196 16.264 11.5126 16.657 11.9946 16.657C12.4766 16.657 12.8696 16.264 12.8696 15.782V11.362Z" fill="currentColor">
                                    </path>
                                    </svg>
                              </span>
                           </a>
                            </div>`;
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
    $('#underReviewRequisitionTable tbody').on('click', 'td.details-control', function (e) {
    e.stopPropagation(); // Prevent the click event from propagating up to the document

    var tr = $(this).closest('tr');
    var row = underReviewRequisitionTable.row(tr);

    // Hide any other shown popovers
    $('.popover').not(this).popover('hide');

    // If the popover is not initialized, create the items list and initialize the popover.
    var items = '';
    for (var i = 0; i < row.data().items.length; i++) {
        items += '<a href="/item-details/' + row.data().items[i].id + '" class="item-link" data-item-id="' + row.data().items[i].id + '">' + row.data().items[i].item_name + ' | Requested Quantity: ' + row.data().items[i].quantity + ' | Approved Quantity In Review: ' + row.data().items[i].approved_quantity + '</a><br>';
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
});
