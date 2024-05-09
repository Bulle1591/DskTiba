// Declare the table as a global variable
var rejectedRequisitionTable;

$(document).ready(function () {
    /* Here begins the DataTable configuration. */
    if ($.fn.dataTable.isDataTable('#rejectedRequisitionTable')) {
        $('#rejectedRequisitionTable').DataTable().destroy();
    }

    rejectedRequisitionTable = $('#rejectedRequisitionTable').DataTable({
        // New initialization options...
        pageLength: 7,
        lengthMenu: [[7, 10, 25, 50, -1], [7, 10, 25, 50, "All"]],
        retrieve: true,
        serverSide: false,
        processing: true,
        full_row_select: true,
        /* Set up the data source */
        ajax: {
            url: "/ajax_datatable/requisitions/rejected/", // Update the URL to point to the endpoint for draft requisitions
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
                            return '<a href="#" data-id="' + row.id + '" onclick="showRejectedRequisitionDetails(this)">' + data + '</a>';
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
                        if(type === 'display'){
                            if(data == 'Pending'){
                                return '<span class="badge bg-soft-warning">' + data + '</span>';
                            } else if(data == 'Approved'){
                                return '<span class="badge bg-soft-success">' + data + '</span>';
                            } else if(data == 'Rejected'){
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

                        if (row.submission_status.toLowerCase() == 'draft') {
                            // If it's a draft, show Edit and Delete buttons
                            buttons = `
                                <div class="d-flex justify-content-center list-user-action">
                                <a class="btn btn-sm btn-icon btn-warning me-1 edit-draft-requisition" data-bs-toggle="tooltip" data-bs-placement="top" data-original-title="Edit" href="/requisition_order/edit/${row.id}/" aria-label="Edit" data-bs-original-title="Edit">
                                  <span class="btn-inner">
                                     <svg class="icon-20" width="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M11.4925 2.78906H7.75349C4.67849 2.78906 2.75049 4.96606 2.75049 8.04806V16.3621C2.75049 19.4441 4.66949 21.6211 7.75349 21.6211H16.5775C19.6625 21.6211 21.5815 19.4441 21.5815 16.3621V12.3341" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                        <path fill-rule="evenodd" clip-rule="evenodd" d="M8.82812 10.921L16.3011 3.44799C17.2321 2.51799 18.7411 2.51799 19.6721 3.44799L20.8891 4.66499C21.8201 5.59599 21.8201 7.10599 20.8891 8.03599L13.3801 15.545C12.9731 15.952 12.4211 16.181 11.8451 16.181H8.09912L8.19312 12.401C8.20712 11.845 8.43412 11.315 8.82812 10.921Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                        <path d="M15.1655 4.60254L19.7315 9.16854" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                     </svg>
                                  </span>
                               </a>
                               <a class="btn btn-sm btn-icon btn btn-danger" data-bs-toggle="tooltip" data-bs-placement="top" href="#" aria-label="Delete" data-bs-original-title="Delete">
                                  <span class="btn-inner">
                                        <svg class="icon-20" width="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path opacity="0.4" d="M19.643 9.48851C19.643 9.5565 19.11 16.2973 18.8056 19.1342C18.615 20.8751 17.4927 21.9311 15.8092 21.9611C14.5157 21.9901 13.2494 22.0001 12.0036 22.0001C10.6809 22.0001 9.38741 21.9901 8.13185 21.9611C6.50477 21.9221 5.38147 20.8451 5.20057 19.1342C4.88741 16.2873 4.36418 9.5565 4.35445 9.48851C4.34473 9.28351 4.41086 9.08852 4.54507 8.93053C4.67734 8.78453 4.86796 8.69653 5.06831 8.69653H18.9388C19.1382 8.69653 19.3191 8.78453 19.4621 8.93053C19.5953 9.08852 19.6624 9.28351 19.643 9.48851Z" fill="currentColor"></path>
                                            <path d="M21 5.97686C21 5.56588 20.6761 5.24389 20.2871 5.24389H17.3714C16.7781 5.24389 16.2627 4.8219 16.1304 4.22692L15.967 3.49795C15.7385 2.61698 14.9498 2 14.0647 2H9.93624C9.0415 2 8.26054 2.61698 8.02323 3.54595L7.87054 4.22792C7.7373 4.8219 7.22185 5.24389 6.62957 5.24389H3.71385C3.32386 5.24389 3 5.56588 3 5.97686V6.35685C3 6.75783 3.32386 7.08982 3.71385 7.08982H20.2871C20.6761 7.08982 21 6.75783 21 6.35685V5.97686Z" fill="currentColor">
                                        </path>
                                        </svg>
                                  </span>
                               </a>
                                </div>`;
                        } else if (row.submission_status.toLowerCase() == 'submitted' && row.approval_status.toLowerCase() == 'approved') {
                            // If it's not a draft and approval status is pending, show Approve and Reject buttons
                            buttons = `
                                <div class="d-flex justify-content-center list-user-action">
                                <a class="btn btn-sm btn-icon btn-info me-1" data-bs-toggle="tooltip" data-bs-placement="top" href="#" aria-label="Approve" data-bs-original-title="Approve">
                                  <span class="btn-inner">
                                    <svg class="icon-20" width="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path opacity="0.4" fill-rule="evenodd" clip-rule="evenodd" d="M17.7366 6.04606C19.4439 7.36388 20.8976 9.29455 21.9415 11.7091C22.0195 11.8924 22.0195 12.1067 21.9415 12.2812C19.8537 17.1103 16.1366 20 12 20H11.9902C7.86341 20 4.14634 17.1103 2.05854 12.2812C1.98049 12.1067 1.98049 11.8924 2.05854 11.7091C4.14634 6.87903 7.86341 4 11.9902 4H12C14.0683 4 16.0293 4.71758 17.7366 6.04606ZM8.09756 12C8.09756 14.1333 9.8439 15.8691 12 15.8691C14.1463 15.8691 15.8927 14.1333 15.8927 12C15.8927 9.85697 14.1463 8.12121 12 8.12121C9.8439 8.12121 8.09756 9.85697 8.09756 12Z" fill="currentColor"></path>                                <path d="M14.4308 11.997C14.4308 13.3255 13.3381 14.4115 12.0015 14.4115C10.6552 14.4115 9.5625 13.3255 9.5625 11.997C9.5625 11.8321 9.58201 11.678 9.61128 11.5228H9.66006C10.743 11.5228 11.621 10.6695 11.6601 9.60184C11.7674 9.58342 11.8845 9.57275 12.0015 9.57275C13.3381 9.57275 14.4308 10.6588 14.4308 11.997Z" fill="currentColor">
                                    </path>
                                    </svg>
                                  </span>
                               </a>
                               <a class="btn btn-sm btn-icon btn-primary" data-bs-toggle="tooltip" data-bs-placement="top" href="#" aria-label="Reject" data-bs-original-title="Reject">
                                  <span class="btn-inner">
                                    <svg class="icon-32" width="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path opacity="0.4" d="M16.34 1.99976H7.67C4.28 1.99976 2 4.37976 2 7.91976V16.0898C2 19.6198 4.28 21.9998 7.67 21.9998H16.34C19.73 21.9998 22 19.6198 22 16.0898V7.91976C22 4.37976 19.73 1.99976 16.34 1.99976Z" fill="currentColor"></path>                                <path fill-rule="evenodd" clip-rule="evenodd" d="M11.1246 8.18921C11.1246 8.67121 11.5156 9.06421 11.9946 9.06421C12.4876 9.06421 12.8796 8.67121 12.8796 8.18921C12.8796 7.70721 12.4876 7.31421 12.0046 7.31421C11.5196 7.31421 11.1246 7.70721 11.1246 8.18921ZM12.8696 11.362C12.8696 10.88 12.4766 10.487 11.9946 10.487C11.5126 10.487 11.1196 10.88 11.1196 11.362V15.782C11.1196 16.264 11.5126 16.657 11.9946 16.657C12.4766 16.657 12.8696 16.264 12.8696 15.782V11.362Z" fill="currentColor">
                                    </path>
                                    </svg>
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
    $('#rejectedRequisitionTable tbody').on('click', 'td.details-control', function (e) {
    e.stopPropagation(); // Prevent the click event from propagating up to the document

    var tr = $(this).closest('tr');
    var row = rejectedRequisitionTable.row(tr);

    // Hide any other shown popovers
    $('.popover').not(this).popover('hide');

    // If the popover is not initialized, create the items list and initialize the popover.
    var items = '';
    for (var i = 0; i < row.data().items.length; i++) {
        items += '<a href="/item-details/' + row.data().items[i].id + '" class="item-link" data-item-id="' + row.data().items[i].id + '">' + row.data().items[i].item_name + ' | Requested Quantity: ' + row.data().items[i].quantity + '</a><br>';
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
