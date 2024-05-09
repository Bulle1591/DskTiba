$(document).on('submit', '#draftToSubmittedForm', function(e) {
    e.preventDefault();
    var url = $("#submitButton").data('url');
    Swal.fire({
        title: "Submit Requisition As Final?",
        text: "Once submitted, you will not be able to change the status back to draft!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: 'Yes, submit it!'
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: url,
                type: 'POST',
                data: $(this).serialize(),
                success: function(response) {
                    if (response.success) {
                        Swal.fire({
                            title: "Success",
                            text: response.message,
                            icon: "success",
                            showCancelButton: true,
                            confirmButtonText: 'Preview',
                            cancelButtonText: 'Close'
                        }).then((result) => {
                            if (result.isConfirmed) {
                                // Open a new tab to generate the preview PDF
                                var previewUrl = '/generate_preview/' + requisitionId + '/';
                                window.open(previewUrl, '_blank');
                            }
                            // Update your page here without a refresh
                            // Close the modal
                            $('#requisitionPreviewModal').modal('hide');
                            // Reload the table
                            $('#draftRequisitionTable').DataTable().ajax.reload();
                            // Reload the table
                            $('#submittedRequisitionTable').DataTable().ajax.reload();
                        });
                    }
                }
            });
        }
    });
});
