$(document).ready(function() {
  $('.btn-submit').click(function(e) {
    e.preventDefault();

    var button = $(this);
    var action = button.data('submit-action');
    var formData = new FormData($('#requisitionOrderForm')[0]);

    // Append 'action' to formData
    formData.append('action', action);

    var confirmationMessage = '';
    if (action === 'save-draft') {
        confirmationMessage = 'Are you sure you want to save this requisition as a draft?';
    } else if (action === 'submit') {
        confirmationMessage = 'Are you sure you want to submit this requisition for approval?';
    }

    // Determine the URL for the AJAX request
    var requisitionId = $('#requisitionId').val();  // Assuming the requisition ID is stored in a hidden input field
    var url = requisitionId ? '/requisition_order/edit/' + requisitionId + '/' : '/requisition_order/new/';

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
                                        // Get the selected requisition type
                                        var requisitionType = $('#id_requisition_type').select2('data')[0].id;

                                        // Determine the preview URL based on the requisition type
                                        var previewUrl;
                                        if (requisitionType === 'store') {
                                            previewUrl = '/generate_preview_store/' + requisitionId + '/';
                                        } else if (requisitionType === 'purchase') {
                                            previewUrl = '/generate_preview_purchase/' + requisitionId + '/';
                                        } else {
                                            // Default preview URL
                                            previewUrl = '/generate_preview/' + requisitionId + '/';
                                        }

                                        // Open a new tab to generate the preview PDF
                                        window.open(previewUrl, '_blank');
                                        window.location.href = '/requisition_order/new/';
                                        window.resetFormset();
                                    }
                                     else {
                                    window.location.href = '/requisition_order/new/';

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
