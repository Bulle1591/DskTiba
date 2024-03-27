
      $(document).ready(function () {
          const element = document.getElementById('addEmployeeModal');
          const form = element.querySelector('#employeeForm');
          const modal = new bootstrap.Modal(element);
          const submitButton = form.querySelector('[data-submit-action="submit"]');
          const nextButton = form.querySelector('[data-next-action="next"]'); // Add this line
          const previousButton = form.querySelector('[data-previous-action="next"]'); // Add this line

          // Initially hide the submit button ad previous
          submitButton.style.display = 'none'; // Add this line
          previousButton.style.display = 'none'; // Add this line

          var validator = FormValidation.formValidation(
          form,
              {
                  fields: {
                      first_name: {
                          validators: {
                              notEmpty: {
                                  message: "First name title can not be empty!"
                              }
                          }
                      },
                      last_name: {
                          validators: {
                              notEmpty: {
                                  message: "Last name can not be empty!"
                              }
                          }
                      },
                      email: {
                          validators: {
                              notEmpty: {
                                  message: "Email can not be empty!"
                              }
                          }
                      },
                      password: {
                          validators: {
                              notEmpty: {
                                  message: "Password can not be empty!"
                              }
                          }
                      }
                  },

                  plugins: {
                      trigger: new FormValidation.plugins.Trigger(),
                      bootstrap: new FormValidation.plugins.Bootstrap5({
                          rowSelector: '.fv-row',
                          eleInvalidClass: '',
                          eleValidClass: ''
                      })
                  }
              }
          );

        // Handle the Next button click event
        $(nextButton).on('click', function(e) {
            e.preventDefault();

            var currentTab, nextTab;
            var fieldValidationPromises = [];

            if ($('.nav-link-home').hasClass('active')) {
                currentTab = $('.tab-home');
                nextTab = $('.tab-profile');
                // Validate only the fields in the home tab
                fieldValidationPromises.push(validator.validateField('first_name'));
                fieldValidationPromises.push(validator.validateField('last_name'));
            } else if ($('.nav-link-profile').hasClass('active')) {
                currentTab = $('.tab-profile');
                nextTab = $('.tab-contact');
                // Validate only the fields in the profile tab

            } else if ($('.nav-link-contact').hasClass('active')) {
                currentTab = $('.tab-contact');
                nextTab = $('.tab-home');
                // Validate only the fields in the contact tab
                fieldValidationPromises.push(validator.validateField('email'));
                fieldValidationPromises.push(validator.validateField('password'));
            }

            // Wait for all field validations to complete
            Promise.all(fieldValidationPromises).then(function(statuses) {
                // Check if all field validations passed
                if (statuses.every(status => status === 'Valid')) {
                    // Your existing tab navigation code...
                    // If it's the last tab
                    if (nextTab.length === 0) {
                        // Show the submit button
                        submitButton.style.display = 'block';
                    } else {
                        // Deactivate the current tab
                        $('.nav-link.active').removeClass('active');
                        currentTab.removeClass('active show');

                        // Activate the next tab
                        if (nextTab.hasClass('tab-profile')) {
                            $('.nav-link-profile').addClass('active');
                             previousButton.style.display = 'block';
                        } else if (nextTab.hasClass('tab-contact')) {
                            $('.nav-link-contact').addClass('active');
                            previousButton.style.display = 'block';
                            submitButton.style.display = 'block';
                            nextButton.style.display = 'none';
                        }
                        nextTab.addClass('active show');
                    }
                } else {
                    // Show the alert if the form is not valid
                    Swal.fire({
                        text: "Please correct the errors in the form before moving to the next step.",
                        icon: "warning",
                        buttonsStyling: false,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn btn-sm btn-100 btn-primary"
                        }
                    });
                }
            });
        });


        // Handle the Previous button click event
        $('[data-previous-action="next"]').on('click', function(e) {
            e.preventDefault();

            var currentTab, prevTab;

            if ($('.nav-link-profile').hasClass('active')) {
                currentTab = $('.tab-profile');
                prevTab = $('.tab-home');
            } else if ($('.nav-link-contact').hasClass('active')) {
                currentTab = $('.tab-contact');
                prevTab = $('.tab-profile');
            }

            // Deactivate the current tab
            $('.nav-link.active').removeClass('active');
            currentTab.removeClass('active show');

            // Activate the previous tab
            if (prevTab.hasClass('tab-home')) {
                $('.nav-link-home').addClass('active');
                previousButton.style.display = 'none';
                nextButton.style.display = 'block';
                submitButton.style.display = 'none';
            } else if (prevTab.hasClass('tab-profile')) {
                $('.nav-link-profile').addClass('active');
                previousButton.style.display = 'block';
                submitButton.style.display = 'none';
                nextButton.style.display = 'block';
            }
            prevTab.addClass('active show');
        });

        // Submit form
        $(form).on('submit', function(e) {
            e.preventDefault();
            validator.validate().then(function(status) {
                if (status === 'Valid') {
                    // Show loading indication
                    submitButton.setAttribute('data-kt-indicator', 'on');

                    var formData = new FormData(form);  // Create new FormData object

                    $.ajax({
                        url: $('#employeeForm').attr('action'),  // the url where we want to POST
                        headers: { "X-CSRFToken": getCookie("csrftoken") },
                        type: 'POST',  // define the type of HTTP verb we want to use (POST for our form)
                        data: new FormData($('#employeeForm')[0]),   // our data object
                        processData: false,  // tell jQuery not to process the data
                        contentType: false,  // tell jQuery not to set contentType
                        success: function(data) {
                            // Hide loading indication
                            submitButton.setAttribute('data-kt-indicator', 'off');

                            if (data.success) {
                                console.log('Form submitted successfully');

                                // Refresh the table
                                loadEmployees()
                                Swal.fire({
                                    text: data.message,  // Display the success message from the server
                                    icon: "success",
                                    buttonsStyling: false,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: {
                                        confirmButton: "btn btn-sm btn-100 btn-primary"
                                    }
                                }).then(function (result) {
                                    if (result.isConfirmed) {
                                        const formElement = document.querySelector('#employeeForm'); // Replace with your form's ID

                                        formElement.reset(); // Reset form
                                        // Close the modal when the user clicks "Ok, got it!"
                                        $('#addEmployeeModal').modal('hide');

                                    }
                                });
                            } else {
                                let errors = '';
                                if (typeof data.error === 'object' && Object.keys(data.error).length > 0) {
                                    $.each(data.error, function(key, value){
                                        errors += '<p>' + key + ': ' + value + '</p>';
                                    });
                                } else {
                                    errors = '<p>An error occurred, but no specific error messages were provided.</p>';
                                }
                                Swal.fire({
                                    icon: 'error',
                                    title: 'Oops...',
                                    html: errors
                                });
                            }
                        },
                        error: function(jqXHR, textStatus, errorThrown) {
                            // Hide loading indication
                            submitButton.setAttribute('data-kt-indicator', 'off');

                            let errors = '';
                            if (jqXHR.responseJSON && jqXHR.responseJSON.error) {
                                $.each(jqXHR.responseJSON.error, function(field, messages){
                                    errors += '<p>' + field + ': ' + messages.join(', ') + '</p>';
                                });
                            } else {
                                errors = '<p>An error occurred, but no specific error messages were provided.</p>';
                            }
                            Swal.fire({
                                icon: 'error',
                                title: 'Oops...',
                                html: errors
                            });
                        }
                    });
                } else {
                    Swal.fire({
                        text: "Please correct the errors in the form before submitting.",
                        icon: "warning",
                        buttonsStyling: false,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn btn-sm btn-100 btn-primary"
                        }
                    });
                }
            });
        });


       // Cancel button handler
          const cancelButton = element.querySelector('[data-cancel-action="cancel"]');
          cancelButton.addEventListener('click', e => {
              e.preventDefault();

              Swal.fire({
                  text: "Are you sure you would like to cancel?",
                  icon: "warning",
                  showCancelButton: true,
                  buttonsStyling: false,
                  confirmButtonText: "Yes, cancel it!",
                  cancelButtonText: "No, return",
                  customClass: {
                      confirmButton: "btn btn-sm btn-100 btn-primary",
                      cancelButton: "btn btn-sm btn-100 btn-active-light"
                  }
              }).then(function (result) {
                  if (result.value) {
                      const formElement = document.querySelector('#employeeForm'); // Replace with your form's ID
                      formElement.reset(); // Reset form
                      validator.resetForm(true); // Reset form validation
                      modal.hide();
                      $('.modal-backdrop').remove();

                  } else if (result.dismiss === 'cancel') {
                      Swal.fire({
                          text: "Your form has not been cancelled!.",
                          icon: "error",
                          buttonsStyling: false,
                          confirmButtonText: "Ok, got it!",
                          customClass: {
                              confirmButton: "btn btn-sm btn-100 btn-primary",
                          }
                      });
                  }
              });
          });

          // Close button handler
          const closeButton = element.querySelector('[data-close-action="close"]');
          closeButton.addEventListener('click', e => {
              e.preventDefault();

              Swal.fire({
                  text: "Are you sure you would like to cancel?",
                  icon: "warning",
                  showCancelButton: true,
                  buttonsStyling: false,
                  confirmButtonText: "Yes, cancel it!",
                  cancelButtonText: "No, return",
                  customClass: {
                      confirmButton: "btn btn-sm btn-100 btn-primary",
                      cancelButton: "btn btn-sm btn-100 btn-active-light"
                  }
              }).then(function (result) {
                  if (result.value) {
                      const formElement = document.querySelector('#employeeForm'); // Replace with your form's ID
                      formElement.reset(); // Reset form
                      validator.resetForm(true); // Reset form validation
                      modal.hide();
                      $('.modal-backdrop').remove();
                  } else if (result.dismiss === 'cancel') {
                      Swal.fire({
                          text: "Your form has not been cancelled!.",
                          icon: "error",
                          buttonsStyling: false,
                          confirmButtonText: "Ok, got it!",
                          customClass: {
                              confirmButton: "btn btn-sm btn-100 btn-primary",
                          }
                      });
                  }
              });
          });
      });


       function getCookie(name) {
          let cookieValue = null;
          if (document.cookie && document.cookie !== '') {
              const cookies = document.cookie.split(';');
              for (let i = 0; i < cookies.length; i++) {
                  const cookie = jQuery.trim(cookies[i]);
                  if (cookie.substring(0, name.length + 1) === (name + '=')) {
                      cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                      break;
                  }
              }
          }
          return cookieValue;
      }
