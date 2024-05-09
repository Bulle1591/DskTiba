function loadEmployees() {
    $.ajax({
        url: '/ajax_card/employee/', // replace with your API endpoint
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            var employeeContainer = $('#employeeContainer'); // replace with your container ID
            employeeContainer.empty(); // clear the container

            // Check if any employees were returned
            if (data.data.length === 0) {
                // No employees were returned, show a SweetAlert2 message
                Swal.fire({
                    title: 'No Employees Found',
                    text: 'Would you like to create a new employee?',
                    icon: 'question',
                    confirmButtonText: 'Create Employee',
                    showCancelButton: true
                }).then((result) => {
                    if (result.isConfirmed) {
                        // User clicked 'Create Employee', open the modal
                        $('#addEmployeeModal').modal('show');
                    }
                });
            } else {
                // Employees were returned, create the cards
                $.each(data.data, function(index, employee) {
                    // ... existing code to create employee cards ...
                    var card = `
                    <div class="col-md-3 col-sm-6 col-12">
                        <div class="card card-flush role-permission-card h-md-100" style="border: none;">
                        <div class="fw-bold text-gray-600 mx-auto p-1">ID #: ${employee.emp_number}</div>
                            <div class="card-header text-center mb-2">
                                <div class="card-title">
                                    <h4>${employee.first_name} ${employee.last_name}</h4>
                                </div>
                                <h6>${employee.designation}</h6>
                            </div>
                            <div class="mx-auto mb-2">
                                <a href="#" data-bs-toggle="modal" data-bs-target="#viewProfileModal${employee.id}">
                                    <img src="${employee.photo[0].photo_file}" alt="Avatar Image" class="rounded-circle w-px-100" />
                                </a>
                            </div>
                            <div class="card-body mx-auto pt-1">
                                <div class="fw-bold text-gray-600">Other Details:</div>
                                <div class="d-flex align-items-center py-1">
                                    <span class="bullet bg-primary me-3"></span> Phone: ${employee.contact[0].phone}
                                </div>
                                <div class="d-flex align-items-center py-1">
                                    <span class="bullet bg-primary me-3"></span> Address: ${employee.contact[0].address}
                                </div>
                            </div>
                            <div class="text-center mb-2">
                                <a href="/employee/view/${employee.id}/" class="btn btn-sm btn-light btn-active-primary my-1 me-2">View Employee</a>
                                <button type="button" class="btn btn-sm btn-light edit-employee btn-active-light-primary my-1" data-bs-toggle="modal" data-bs-target="#addEmployeeModal" data-employee-id="${employee.id}">Edit Employee</button>
                            </div>
                        </div>
                    </div>
                `;
                employeeContainer.append(card);
                });
            }
        }
    });
}

// Call the function when the page loads
$(document).ready(function() {
    loadEmployees();
});
