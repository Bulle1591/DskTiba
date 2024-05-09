$(document).ready(function() {
  $('.btn-submit').click(function(e) {
    e.preventDefault();

    var button = $(this);
    var action = button.data('submit-action');  // Get the action from the button's data-submit-action attribute
    var formData = new FormData($('#ManageRequisitionOrderForm')[0])

    // Append 'action' to formData
    formData.append('action', action);

    var confirmationMessage = '';
    if (action === 'reject') {
        confirmationMessage = 'Are you sure you want to reject this requisition order?';
    } else if (action === 'approve') {
        confirmationMessage = 'Are you sure you want to approve this requisition order?';
    } else if (action === 'under-review') {
        confirmationMessage = 'Are you sure you want to mark this requisition order as under review?';
    }

    // Determine the URL for the AJAX request
    var requisitionId = $('#requisitionId').val();  // Assuming the requisition ID is stored in a hidden input field
    var url = '/store_requisition_order/manage/' + requisitionId + '/';

    Swal.fire({
        icon: 'question',
        title: 'Confirmation',
        text: confirmationMessage,
        showCancelButton: true,
        confirmButtonText: 'Yes',
        cancelButtonText: 'No'
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: url,
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                    if (response.success) {
                        Swal.fire({
                            icon: 'success',
                            title: 'Success!',
                            text: response.message,
                            showCancelButton: true,
                            confirmButtonText: 'Preview',
                            cancelButtonText: 'Close'
                        }).then((result) => {
                                if (result.isConfirmed) {
                                    // Open a new tab to generate the preview PDF
                                    var previewUrl = '/generate_preview/' + requisitionId + '/';
                                    window.open(previewUrl, '_blank');
                                } else {
                                    button.prop('disabled', true);
                                }
                            });
                        } else {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error!',
                            text: response.message,
                        });
                    }
                    // Call the removeAllRows function to reset the form and remove all rows
                    // window.resetFormset();
                },
                          error: function(error) {
                    var errorMessage = 'An error occurred while submitting the requisition.';
                    if (error.status === 400) {
                        var errors = JSON.parse(error.responseText);
                        errorMessage = '';
                        if (errors.form_errors && errors.form_errors != '{}') {
                            errorMessage += 'Form Errors: ' + errors.form_errors + '<br>';
                        }
                        if (errors.formset_errors && errors.formset_errors != '[]') {
                            errorMessage += 'Formset Errors: ' + errors.formset_errors + '<br>';
                        }
                    } else if (error.status === 403) {
                        errorMessage = 'You do not have permission to perform this action.';
                    } else if (error.status === 500) {
                        errorMessage = 'An unexpected error occurred on the server.';
                    }
                    Swal.fire({
                        icon: 'error',
                        title: 'Error!',
                        html: errorMessage,
                    });
                }
            });
        }
    });
  });
});
