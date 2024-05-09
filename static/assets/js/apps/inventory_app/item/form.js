
  $(document).ready(function () {
      const element = document.getElementById('itemModal');
      const modal = new bootstrap.Modal(element);
      const form = document.querySelector('#itemForm');
      const submitButton = form.querySelector('[data-submit-action="submit"]');

      var validator = FormValidation.formValidation(
      form,
          {
              fields: {
                  name: {
                      validators: {
                          notEmpty: {
                              message: "Name can not be empty!"
                          }
                      }
                  },
                  item_type: {
                      validators: {
                          notEmpty: {
                              message: "Type can not be empty!"
                          }
                      }
                  },
                  reorder_level: {
                      validators: {
                          notEmpty: {
                              message: "Reorder level can not be empty!"
                          }
                      }
                  },
                  alert_quantity: {
                      validators: {
                          notEmpty: {
                              message: "Alert Quantity can not be empty!"
                          }
                      }
                  },
                   unit_of_measure: {
                      validators: {
                          notEmpty: {
                              message: "Unit can not be empty!"
                          }
                      }
                  },
                  supplier: {
                      validators: {
                          notEmpty: {
                              message: "Supplier can not be empty!"
                          }
                      }
                  },
                  category: {
                      validators: {
                          notEmpty: {
                              message: "Category can not be empty!"
                          }
                      }
                  },
                  subcategory: {
                      validators: {
                          notEmpty: {
                              message: "Subcategory can not be empty!"
                          }
                      }
                  },
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


      // Submit form
      $(form).on('submit', function(e) {
          e.preventDefault();
          validator.validate().then(function(status) {
              if (status === 'Valid') {
                  // Show loading indication
                  submitButton.setAttribute('data-kt-indicator', 'on');

                  var formData = new FormData(form);  // Create new FormData object

                  $.ajax({
                    url: $('#itemForm').attr('action'),  // the url where we want to POST
                      headers: { "X-CSRFToken": getCookie("csrftoken") },
                      type: 'POST',  // define the type of HTTP verb we want to use (POST for our form)
                      data: new FormData($('#itemForm')[0]),   // our data object
                      processData: false,  // tell jQuery not to process the data
                      contentType: false,  // tell jQuery not to set contentType
                      success: function(data) {
                          // Hide loading indication
                          submitButton.setAttribute('data-kt-indicator', 'off');

                          if (data.success) {
                              console.log('Form submitted successfully');

                              // Refresh the table
                              itemTable.ajax.reload()
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
                                      const formElement = document.querySelector('#itemForm'); // Replace with your form's ID
                                      formElement.reset(); // Reset form
                                      modal.hide(); // Hide modal
                                      $('.modal-backdrop').remove();
                                      // Reset each Select2 dropdown in the form
                                      $('#id_supplier').val(null).trigger('change');
                                      $('#id_category').val(null).trigger('change');
                                      $('#id_subcategory').val(null).trigger('change');
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

   // Cancel button handler
    const cancelButton = document.querySelector('[data-cancel-action="reset"]');
    cancelButton.addEventListener('click', e => {
        e.preventDefault();

        Swal.fire({
            text: "Are you sure you would like to reset form?",
            icon: "warning",
            showCancelButton: true,
            buttonsStyling: false,
            confirmButtonText: "Yes, reset it!",
            cancelButtonText: "No, return",
            customClass: {
                confirmButton: "btn btn-sm btn-100 btn-primary me-2",
                cancelButton: "btn btn-sm btn-100 btn-light"
            }
        }).then(function (result) {
            if (result.value) {
                const formElement = document.querySelector('#itemForm'); // Replace with your form's ID

                // Reset form
                formElement.reset();

                // Reset form validation
                validator.resetForm(true);

                 // Reset each Select2 dropdown in the form
                $('#id_supplier').val(null).trigger('change');
                $('#id_category').val(null).trigger('change');
                $('#id_subcategory').val(null).trigger('change');
            } else if (result.dismiss === 'cancel') {
                Swal.fire({
                    text: "Your form has not been cleared!.",
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

    // Cancel button handler
    const closeButton = document.querySelector('[data-cancel-action="close"]');
    closeButton.addEventListener('click', e => {
        e.preventDefault();

        Swal.fire({
            text: "Are you sure you would like to close form?",
            icon: "warning",
            showCancelButton: true,
            buttonsStyling: false,
            confirmButtonText: "Yes, close it!",
            cancelButtonText: "No, return",
            customClass: {
                confirmButton: "btn btn-sm btn-100 btn-primary me-2",
                cancelButton: "btn btn-sm btn-100 btn-light"
            }
        }).then(function (result) {
            if (result.value) {
                const formElement = document.querySelector('#itemForm'); // Replace with your form's ID

                // Reset form
                formElement.reset();

                modal.hide();
                $('.modal-backdrop').remove();

                // Reset form validation
                validator.resetForm(true);
                 // Reset each Select2 dropdown in the form
                $('#id_supplier').val(null).trigger('change');
                $('#id_category').val(null).trigger('change');
                $('#id_subcategory').val(null).trigger('change');
            } else if (result.dismiss === 'cancel') {
                Swal.fire({
                    text: "Your form has not been closed!.",
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
