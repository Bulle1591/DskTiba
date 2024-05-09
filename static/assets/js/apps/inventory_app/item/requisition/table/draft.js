// Declare the table as a global variable
var draftRequisitionTable;

$(document).ready(function () {
    /* Here begins the DataTable configuration. */
    if ($.fn.dataTable.isDataTable('#draftRequisitionTable')) {
        $('#draftRequisitionTable').DataTable().destroy();
    }

    draftRequisitionTable = $('#draftRequisitionTable').DataTable({
        // New initialization options...
        pageLength: 7,
        lengthMenu: [[7, 10, 25, 50, -1], [7, 10, 25, 50, "All"]],
        retrieve: true,
        serverSide: false,
        processing: true,
        full_row_select: true,
        /* Set up the data source */
        ajax: {
            url: "/ajax_datatable/requisitions/draft/", // Update the URL to point to the endpoint for draft requisitions
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
                            return '<a href="#" data-id="' + row.id + '" onclick="showDraftRequisitionDetails(this)">' + data + '</a>';
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
                    "data": "submission_status",
                    "render": function ( data, type, row, meta ) {
                        if(type === 'display' && data == 'Draft'){
                            return '<span class="badge bg-soft-warning">' + data + '</span>';
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
                            <a class="btn btn-sm btn-icon btn-info me-1 edit-draft-requisition" data-bs-toggle="tooltip" data-bs-placement="top" data-original-title="Edit" href="/requisition_order/edit/${row.id}/" aria-label="Edit" data-bs-original-title="Edit">
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
                        return buttons;
                    }
                }
            ],

        rowCallback: function(row, data) {
        // Assign the ID of the data item to the row
        $(row).data('id', data.id);
        },

        drawCallback: function(settings) {
        $('[data-bs-toggle="tooltip"]').tooltip();
        },
    });

    // Add event listener for opening and closing details(USE POPUPS)
    $('#draftRequisitionTable tbody').on('click', 'td.details-control', function (e) {
    e.stopPropagation(); // Prevent the click event from propagating up to the document

    var tr = $(this).closest('tr');
    var row = draftRequisitionTable.row(tr);

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
