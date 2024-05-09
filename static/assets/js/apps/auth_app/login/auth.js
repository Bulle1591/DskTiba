$(document).ready(function() {
    $('#authenticationForm').on('submit', function(event) {
        event.preventDefault();

        var email = $('#email-id').val();
        var password = $('#password').val();

        console.log(`Email: ${email}, Password: ${password}`);  // Debugging statement

        if (!email && !password) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Email and password are required.'
            });
            return;
        }

        if (!email) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Email is required.'
            });
            return;
        }

        if (!password) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Password is required.'
            });
            return;
        }

        // Show loading indication
        var submitButton = this.querySelector('[data-submit-action="submit"]');
        submitButton.setAttribute('data-kt-indicator', 'on');

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: $(this).serialize(),
            dataType: 'json',
            success: function(data) {
                console.log(`Success response: ${JSON.stringify(data)}`);  // Debugging statement
                if (data.success) {
                    window.location.href = "/dashboard/";
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: data.error
                    });
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log(`Error response: ${jqXHR.status}, ${textStatus}, ${errorThrown}`);  // Debugging statement
                var errorMessage = 'An error occurred while processing your request. Please try again.';
                if (jqXHR.status === 400) {
                    errorMessage = 'There might be issues with your email or password. Please check and try again.';
                }
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: errorMessage
                });
            },
            complete: function() {
                // Hide loading indication
                submitButton.setAttribute('data-kt-indicator', 'off');
            }
        });
    });
});
