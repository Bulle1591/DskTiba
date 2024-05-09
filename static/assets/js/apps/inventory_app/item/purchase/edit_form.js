
     $(document).ready(function () {
          const form = document.querySelector('#purchaseOrderForm');
          const submitButton = form.querySelector('[data-submit-action="submit"]');

     var validator = FormValidation.formValidation(
        form,
        {
            fields: {
                supplier: {
                    validators: {
                        notEmpty: {
                            message: "Supplier can not be empty!"
                        }
                    }
                },
                expected_delivery_date: {
                    validators: {
                        notEmpty: {
                            message: "Delivered date can not be empty!"
                        }
                    }
                },
                status: {
                    validators: {
                        notEmpty: {
                            message: "Status can not be empty!"
                        }
                    }
                },
                // Add a custom field for the formset
                formset: {
                    validators: {
                        callback: {
                            message: 'Please fill out at least one form completely before submitting.',
                            callback: function(input) {
                                var isValid = false;
                                $('.item-formset').each(function() {
                                    var isFormFilled = true;
                                    $(this).find('input,select').each(function() {
                                        if ($(this).val() === '') {
                                            isFormFilled = false;
                                            return false; // Break the loop
                                        }
                                    });
                                    if (isFormFilled) {
                                        isValid = true;
                                        return false; // Break the loop
                                    }
                                });
                                if (!isValid) {
                                    Swal.fire({
                                        icon: 'error',
                                        title: 'Oops...',
                                        text: 'Please fill out at least one form completely before submitting.',
                                    });
                                }
                                return isValid;
                            }
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



      // Submit updated form
      $(form).on('submit', function(e) {
          e.preventDefault();
          validator.validate().then(function(status) {
              if (status === 'Valid') {
                  // Show loading indication
                  submitButton.setAttribute('data-kt-indicator', 'on');

                  var formData = new FormData(form);  // Create new FormData object

                  $.ajax({
                    url: $('#purchaseOrderForm').attr('action'),  // the url where we want to POST
                      headers: { "X-CSRFToken": getCookie("csrftoken") },
                      type: 'POST',  // define the type of HTTP verb we want to use (POST for our form)
                      data: new FormData($('#purchaseOrderForm')[0]),   // our data object
                      processData: false,  // tell jQuery not to process the data
                      contentType: false,  // tell jQuery not to set contentType
                      success: function(data) {
                          // Hide loading indication
                          submitButton.setAttribute('data-kt-indicator', 'off');

                          if (data.success) {
                              console.log('Form submitted successfully');

                              // Refresh PurchaseItem table
                              // purchaseItemTable.ajax.reload()
                              // Refresh Purchase Order table
                              // purchaseOrderTable.ajax.reload()
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
                                      const formElement = document.querySelector('#purchaseOrderForm'); // Replace with your form's ID

                                      // formElement.reset(); // Reset form
                                      // Reset each Select2 dropdown in the form
                                      // $('#id_supplier').val(null).trigger('change');
                                      // $('#id_status').val(null).trigger('change');

                                  }
                              });
                          }
                           else {
                              let errors = '';
                              if (typeof data.error === 'object' && Object.keys(data.error).length > 0) {
                                  $.each(data.error, function(key, value){
                                      errors += '<p>' + value + '</p>';
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

                          Swal.fire({
                              icon: 'error',
                              title: 'Oops...',
                              text: 'Something went wrong!'
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
