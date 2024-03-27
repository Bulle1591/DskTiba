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
                <div class="col-xl-4 col-lg-6 col-md-6">
                    <div class="card role-permission-card">
                      <div class="card-body">
                        <div class="d-flex justify-content-between mb-2">
                          <h6 class="fw-normal">Total ${role.total_users} users</h6>

                          <ul class="list-unstyled d-flex align-items-center avatar-group mb-0">`;
                            // loop through the users in the role
                            $.each(role.users, function(index, user) {
                                card += `
                                    <li data-bs-toggle="tooltip" data-popup="tooltip-custom" data-bs-placement="top" title="${user.name}" class="avatar avatar-sm pull-up">
                                        <img class="rounded-circle" src="${user.image_url}" alt="Avatar">
                                    </li>
                                `;
                            });
                            card += `
                        </ul>

                        </div>
                        <div class="d-flex justify-content-between align-items-end">
                          <div class="role-heading">
                            <h4 class="role-name mb-1">${role.name}</h4>
                            <h6 class="role-description" style="display: none;">${role.description}</h6>
                            <a href="javascript:void(0);" class="edit-role me-5" data-bs-toggle="modal" data-bs-target="#addRoleModal" data-role-id="${role.id}" data-role-permissions='${JSON.stringify(role.permissions)}'><small>Edit Role</small></a>
                            <a href="/role/view/${role.id}/"><small>View Role</small></a>
                          </div>
                          <a href="javascript:void(0);" class="text-muted">
                              <svg width="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path opacity="0.4" d="M16.34 1.99976H7.67C4.28 1.99976 2 4.37976 2 7.91976V16.0898C2 19.6198 4.28 21.9998 7.67 21.9998H16.34C19.73 21.9998 22 19.6198 22 16.0898V7.91976C22 4.37976 19.73 1.99976 16.34 1.99976Z" fill="currentColor"></path>
                                <path d="M15.0158 13.7703L13.2368 11.9923L15.0148 10.2143C15.3568 9.87326 15.3568 9.31826 15.0148 8.97726C14.6728 8.63326 14.1198 8.63426 13.7778 8.97626L11.9988 10.7543L10.2198 8.97426C9.87782 8.63226 9.32382 8.63426 8.98182 8.97426C8.64082 9.31626 8.64082 9.87126 8.98182 10.2123L10.7618 11.9923L8.98582 13.7673C8.64382 14.1093 8.64382 14.6643 8.98582 15.0043C9.15682 15.1763 9.37982 15.2613 9.60382 15.2613C9.82882 15.2613 10.0518 15.1763 10.2228 15.0053L11.9988 13.2293L13.7788 15.0083C13.9498 15.1793 14.1728 15.2643 14.3968 15.2643C14.6208 15.2643 14.8448 15.1783 15.0158 15.0083C15.3578 14.6663 15.3578 14.1123 15.0158 13.7703Z" fill="currentColor"></path>
                              </svg>
                            </a>
                        </div>
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
