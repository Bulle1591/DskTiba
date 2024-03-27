function loadRoles() {
    $.ajax({
        url: '/ajax_card/role/', // replace with your API endpoint
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            var roleContainer = $('#roleContainer'); // replace with your container ID
            roleContainer.empty(); // clear the container

            // loop through the data and create the cards
            $.each(data, function(index, role) {
            var permissions = role.permissions.slice(0, 4);
            var morePermissionsCount = Math.max(role.permissions.length - 4, 0);
            var card = `
                <div class="col-md-3">
                    <div class="card card-flush role-permission-card h-md-100" style="height: 350px; border: none;">
                        <div class="card-header mb-3">
                            <div class="card-title">
                                <h4 class="role-name">${role.name}</h4>
                            </div>
                            <h6 class="role-description">${role.description}</h6>
                        </div>

                        <div class="card-body pt-1">
                            <div class="fw-bold text-gray-600 mb-3">Total users with this role: ${role.total_users}</div>
                            ${permissions.map(permission => `
                                <div class="d-flex align-items-center py-1">
                                    <span class="bullet bg-primary me-3"></span> ${permission.name}
                                </div>
                            `).join('')}
                            ${morePermissionsCount > 0 ? `<div class="d-flex align-items-center py-2"><span class="bullet bg-primary me-3"></span><em>and ${morePermissionsCount} more...</em></div>` : ''}
                        </div>
                        <div class="text-center mb-3">
                            <a href="/role/view/${role.id}/" class="btn btn-sm btn-light custom-form-action-button btn-active-primary my-1 me-2">View Role</a>

                            <button type="button" class="btn btn-sm btn-light edit-role-permissions custom-form-action-button btn-active-light-primary my-1" data-bs-toggle="modal" data-bs-target="#addRoleModal" data-role-id="${role.id}" data-role-permissions='${JSON.stringify(role.permissions)}'>Edit Role</button>
                        </div>
                    </div>
                </div>
            `;
            roleContainer.append(card);
        });

        }
    });
}

// Call the function when the page loads
$(document).ready(function() {
    loadRoles();
});
