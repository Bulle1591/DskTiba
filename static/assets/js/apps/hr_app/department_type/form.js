
  $(document).ready(function () {
      const element = document.getElementById('departmentTypeModal');
      const form = element.querySelector('#departmentTypeForm');
      const modal = new bootstrap.Modal(element);
      const submitButton = form.querySelector('[data-submit-action="submit"]');

      var validator = FormValidation.formValidation(
      form,
          {
              fields: {
                  name: {
                      validators: {
                          notEmpty: {
                              message: "Department type name can not be empty!"
                          }
                      }
                  },
                  code: {
                      validators: {
                          notEmpty: {
                              message: "Department code can not be empty!"
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
      // Define the custom validator

      // Submit form
      $(form).on('submit', function(e) {
          e.preventDefault();
          validator.validate().then(function(status) {
              if (status === 'Valid') {
                  // Show loading indication
                  submitButton.setAttribute('data-kt-indicator', 'on');

                  var formData = new FormData(form);  // Create new FormData object

                  $.ajax({
                    url: $('#departmentTypeForm').attr('action'),  // the url where we want to POST
                      headers: { "X-CSRFToken": getCookie("csrftoken") },
                      type: 'POST',  // define the type of HTTP verb we want to use (POST for our form)
                      data: new FormData($('#departmentTypeForm')[0]),   // our data object
                      processData: false,  // tell jQuery not to process the data
                      contentType: false,  // tell jQuery not to set contentType
                      success: function(data) {
                          // Hide loading indication
                          submitButton.setAttribute('data-kt-indicator', 'off');

                          if (data.success) {
                              console.log('Form submitted successfully');

                              // Refresh the table
                              departmentTypeTable.ajax.reload()
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
                                      const formElement = document.querySelector('#departmentTypeForm'); // Replace with your form's ID

                                      formElement.reset(); // Reset form
                                      // Close the modal when the user clicks "Ok, got it!"
                                      $('#departmentTypeModal').modal('hide');

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
                  const formElement = document.querySelector('#departmentTypeForm'); // Replace with your form's ID
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
                  const formElement = document.querySelector('#departmentTypeForm'); // Replace with your form's ID
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
