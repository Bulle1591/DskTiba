$(document).ready(function() {
    $('#purchaseOrderForm').on('submit', function(e) {
        e.preventDefault();

        // Show loading indicator
        $('#submit').attr('disabled', true);
        $('#submit .indicator-label').hide();
        $('#submit .indicator-progress').show();

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: $(this).serialize(),
            success: function(data) {
            // Hide loading indicator
            $('#submit').attr('disabled', false);
            $('#submit .indicator-label').show();
            $('#submit .indicator-progress').hide();

            if (data.success) {
                Swal.fire({
                    title: 'Success!',
                    text: data.message,
                    icon: 'success',
                    confirmButtonText: 'OK'
                });
            } else {
                var message = data.message;
                if (data.form_errors) {
                    var formErrors = JSON.parse(data.form_errors);
                    message += "\nForm errors: " + JSON.stringify(formErrors, null, 2);
                }
                if (data.formset_errors) {
                    var formsetErrors = JSON.parse(data.formset_errors);
                    message += "\nFormset errors: " + JSON.stringify(formsetErrors, null, 2);
                }

                Swal.fire({
                    title: 'Error!',
                    text: message,
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        },
        error: function(xhr, status, error) {
            // Hide loading indicator
            $('#submit').attr('disabled', false);
            $('#submit .indicator-label').show();
            $('#submit .indicator-progress').hide();

            Swal.fire({
                title: 'Error!',
                text: 'An error occurred while processing your request.',
                icon: 'error',
                confirmButtonText: 'OK'
            });
        }
        });
    });
});
