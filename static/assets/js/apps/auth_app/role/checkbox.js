document.addEventListener('DOMContentLoaded', (event) => {
    // Handle the "Check All" checkbox
    const checkAllCheckbox = document.getElementById('check_all');
    checkAllCheckbox.addEventListener('change', (event) => {
        Swal.fire({
            title: 'Are you sure?',
            text: 'You are about to ' + (event.target.checked ? 'check' : 'uncheck') + ' all permissions!',
            icon: 'warning',
            showCancelButton: true,
            buttonsStyling: false,
            confirmButtonText: 'Yes, do it!',
            cancelButtonText: 'No, cancel!',
             customClass: {
                  confirmButton: "btn btn-sm btn-100 btn-primary",
                  cancelButton: "btn btn-sm btn-100 btn-light"
              }
        }).then((result) => {
            if (result.isConfirmed) {
                // Select only the permission checkboxes when "Check All" is checked
                // Select all checkboxes when "Check All" is unchecked
                const checkboxes = document.querySelectorAll(`input[type="checkbox"]${event.target.checked ? ':not([id^="select_all_"])' : ''}`);
                checkboxes.forEach((checkbox) => {
                    checkbox.checked = event.target.checked;
                });

                // If "Check All" is unchecked, also uncheck "Select All" checkboxes
                if (!event.target.checked) {
                    const selectAllCheckboxes = document.querySelectorAll('input[id^="select_all_"]');
                    selectAllCheckboxes.forEach((checkbox) => {
                        checkbox.checked = false;
                    });
                }
            } else {
                // If the user cancels, revert the "Check All" checkbox state
                event.target.checked = !event.target.checked;
            }
        });
    });

    // Handle each "Select All" checkbox
    const selectAllCheckboxes = document.querySelectorAll('input[id^="select_all_"]');
    selectAllCheckboxes.forEach((selectAllCheckbox) => {
        selectAllCheckbox.addEventListener('change', (event) => {
            Swal.fire({
                title: 'Are you sure?',
                text: 'You are about to ' + (event.target.checked ? 'check' : 'uncheck') + ' all permissions for this module!',
                icon: 'warning',
                showCancelButton: true,
                buttonsStyling: false,
                confirmButtonText: 'Yes, do it!',
                cancelButtonText: 'No, cancel!',
                customClass: {
                  confirmButton: "btn btn-sm btn-100 btn-primary",
                  cancelButton: "btn btn-sm btn-100 btn-light"
              }
            }).then((result) => {
                if (result.isConfirmed) {
                    // Uncheck all other checkboxes
                    const otherCheckboxes = document.querySelectorAll(`input[type="checkbox"]:not(#${event.target.id})`);
                    otherCheckboxes.forEach((checkbox) => {
                        checkbox.checked = false;
                    });

                    // Check or uncheck all checkboxes for this module
//                    const module = event.target.id.replace('select_all_', '');
//                    const checkboxes = document.querySelectorAll(`input[id^="${module}"]:not([id^="select_all_"])`);
//                    checkboxes.forEach((checkbox) => {
//                        checkbox.checked = event.target.checked;
//                    });

                    // Check or uncheck all checkboxes for this permission
                    const permissionId = event.target.id.replace('select_all_', '');
                    const checkboxes = document.querySelectorAll(`input[id^="select_all_${module}"]:not([id^="select_all_"])`);
                    checkboxes.forEach((checkbox) => {
                        checkbox.checked = event.target.checked;
                    });

                } else {
                    // If the user cancels, revert the "Select All" checkbox state
                    event.target.checked = !event.target.checked;
                }
            });
        });
    });
});
